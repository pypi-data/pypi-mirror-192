import logging
import typing as t
import weakref

ObjectID = t.Union[int, t.Tuple[int, int]]

NONE_ID = id(None)


def _make_id(target) -> ObjectID:
    if target is None:
        return NONE_ID
    if hasattr(target, "__func__"):
        return id(target.__self__), id(target.__func__)
    return id(target)


class LookupKey(t.NamedTuple):
    receiver_id: ObjectID
    sender_id: ObjectID


Receiver = t.Union[weakref.ReferenceType, t.Callable]
References = t.Dict[LookupKey, Receiver]

logger = logging.getLogger(__name__)


class Signal:
    __slots__ = ("_references",)

    def __init__(self) -> None:
        self._references: References = {}

    def _live_receivers(self, sender: t.Any = None) -> t.Generator[t.Tuple[LookupKey, t.Callable], None, None]:
        sender_id = _make_id(sender)
        for key in tuple(self._references.keys()):
            func = self._references[key]
            if isinstance(func, weakref.ReferenceType):
                func = func()
            if func:
                if key.sender_id == NONE_ID or key.sender_id == sender_id:
                    yield key, func
            else:
                del self._references[key]

    def connect(self, func: t.Callable = None, sender: t.Any = None, weak: bool = True) -> t.Optional[t.Callable]:
        if not func:
            return lambda f: self.connect(f, sender=sender, weak=weak)
        key = LookupKey(_make_id(func), _make_id(sender))
        if key not in self._references:
            if weak:
                ref_type: t.Type[weakref.ReferenceType] = weakref.ref
                if hasattr(func, "__self__") and hasattr(func, "__func__"):
                    ref_type = weakref.WeakMethod
                self._references[key] = ref_type(func)
            else:
                self._references[key] = func
        return func

    def disconnect(self, func: t.Callable) -> bool:
        for key, receiver in self._live_receivers():
            if func == receiver:
                del self._references[key]
                return True
        return False

    def clear(self) -> None:
        self._references.clear()

    def send(self, sender=None, **kwargs: t.Any) -> t.List[t.Any]:
        responses = []
        for _, receiver in self._live_receivers(sender):
            res = receiver(sender=sender, **kwargs)
            if res:
                responses.append(res)
        return responses

    def send_robust(self, sender=None, **kwargs: t.Any) -> t.List[t.Any]:
        responses = []
        for _, receiver in self._live_receivers(sender):
            try:
                res = receiver(sender=sender, **kwargs)
            except Exception as e:
                logger.error(
                    "Error calling %s in Signal.send_robust() (%s)",
                    receiver.__qualname__,
                    e,
                    exc_info=e,
                )
            else:
                if res:
                    responses.append(res)
        return responses
