from contextlib import suppress
from threading import Lock

from bundlewrap.exceptions import BundleError
from bundlewrap.items import BUILTIN_ITEM_ATTRIBUTES, Item
from bundlewrap.operations import RunResult
from bundlewrap.utils.ui import io
from bundlewrap.utils.text import mark_for_translation as _

from librouteros import connect


# very basic connection management, connections are never closed (unless
# on errors)
CONNECTIONS = {}
CONNECTION_LOCK = Lock()


class RouterOS(Item):
    """
    RouterOS configuration.
    """
    BUNDLE_ATTRIBUTE_NAME = "routeros"
    ITEM_ATTRIBUTES = {
        'delete': False,
    }
    ITEM_TYPE_NAME = "routeros"
    REJECT_UNKNOWN_ATTRIBUTES = False

    @classmethod
    def block_concurrent(cls, node_os, node_os_version):
        return [cls.ITEM_TYPE_NAME]

    def __repr__(self):
        return f"<RouterOS {self.name}>"

    def cdict(self):
        if self.attributes['delete']:
            return None
        cdict = self.attributes.copy()
        if '_comment' in cdict:  # work around 'comment' being a builtin attribute
            cdict['comment'] = cdict['_comment']
            del cdict['_comment']
        del cdict['delete']
        return cdict

    def fix(self, status):
        if status.must_be_created:
            self._add(self.name.split("?", 1)[0], status.cdict)
        elif status.must_be_deleted:
            self._remove(self.name.split("?", 1)[0], status.sdict['.id'])
        else:
            for key in status.keys_to_fix:
                self._set(
                    self.name.split("?", 1)[0],
                    status.sdict.get('.id'),
                    key,
                    status.cdict[key],
                )

    def sdict(self):
        result = self._get(self.name)
        if result:
            # API doesn't return comment at all if emtpy
            result.setdefault('comment', '')
            # undo automatic type conversion in librouteros
            for key, value in tuple(result.items()):
                if value is True:
                    result[key] = "true"
                elif value is False:
                    result[key] = "false"
                elif isinstance(value, int):
                    result[key] = str(value)
        return result

    def display_on_create(self, cdict):
        for key in tuple(cdict.keys()):
            if cdict[key].count(",") > 2:
                cdict[key] = cdict[key].split(",")
        return cdict

    def display_dicts(self, cdict, sdict, keys):
        for key in keys:
            if cdict[key].count(",") > 2 or sdict[key].count(",") > 2:
                cdict[key] = cdict[key].split(",")
                sdict[key] = sdict[key].split(",")
        return (cdict, sdict, keys)

    def display_on_delete(self, sdict):
        with suppress(KeyError):
            del sdict[".id"]
        for key in tuple(sdict.keys()):
            if sdict[key].count(",") > 2:
                sdict[key] = sdict[key].split(",")
        return sdict

    def patch_attributes(self, attributes):
        for key in tuple(attributes.keys()):
            if key in BUILTIN_ITEM_ATTRIBUTES:
                continue
            value = attributes[key]
            if value is True:
                attributes[key] = "true"
            elif value is False:
                attributes[key] = "false"
            elif isinstance(value, set):
                attributes[key] = ",".join(sorted(value))
            elif isinstance(value, (tuple, list)):
                attributes[key] = ",".join(value)
            elif isinstance(value, int):
                attributes[key] = str(value)
        return attributes

    @property
    def _connection(self):
        try:
            connection = CONNECTIONS[self.node]
        except KeyError:
            connection = connect(
                # str() to resolve Faults
                username=str(self.node.username),
                password=str(self.node.password or ""),
                host=self.node.hostname,
                timeout=120.0,
            )
            CONNECTIONS[self.node] = connection
        return connection

    def _run(self, *args):
        with CONNECTION_LOCK:
            try:
                io.debug(f'{self.node.name}: running routeros command: {repr(args)}')
                result = tuple(self._connection.rawCmd(*args))
            except Exception as e:
                # Connection in unknown state, try to close it and then
                # drop it.
                try:
                    self._connection.close()
                except Exception:
                    pass
                del CONNECTIONS[self.node]
                raise e
            run_result = RunResult()
            run_result.stdout = repr(result)
            run_result.stderr = ""

            self._command_results.append({
                'command': repr(args),
                'result': run_result,
            })
            return result

    def _add(self, command, kwargs):
        identifier = self.name.split("?", 1)[1]
        for identifier_component in identifier.split("&"):
            identifier_key, identifier_value = identifier_component.split("=", 1)
            kwargs[identifier_key] = identifier_value
        command += "/add"
        arguments = [f"={key}={value}" for key, value in kwargs.items()]
        self._run(command, *arguments)

    def _get(self, command):
        if "?" in command:
            command, query = command.split("?", 1)
            query = query.split("&")
            query = ["?=" + condition for condition in query]
            query.append("?#&")  # AND all conditions
            result = self._run(command + "/print", *query)
        else:
            result = self._run(command + "/print")

        if not result:
            return None
        elif len(result) == 1:
            return result[0]
        else:
            raise BundleError(_(
                "{item} on {node} returned ambiguous data from API: {result}"
            ).format(
                item=self.id,
                node=self.node.name,
                result=repr(result),
            ))

    def _set(self, command, api_id, key, value):
        command += "/set"
        kvstr = f"={key}={value}"
        if api_id is None:
            self._run(command, kvstr)
        else:
            self._run(command, f"=.id={api_id}", kvstr)

    def _remove(self, command, api_id):
        self._run(command + "/remove", f"=.id={api_id}")
