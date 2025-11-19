from typing import Callable, Dict, List, Type, Any, Iterable, Deque
from collections import deque

__all__ = ["EventBus"]

Handler = Callable[[Any], Any]

class EventBus:
    def __init__(self) -> None:
        self._subs: Dict[Type[Any], List[tuple[int, bool, Handler]]] = {}
        self._subs_all: List[tuple[int, bool, Handler]] = []

    def subscribe(self, event_type: Type[Any], handler: Handler, *, priority: int = 0, once: bool = False) -> None:
        lst = self._subs.setdefault(event_type, [])
        lst.append((priority, once, handler))
        lst.sort(key=lambda x: x[0], reverse=True)

    def subscribe_all(self, handler: Handler, *, priority: int = -10, once: bool = False) -> None:
        self._subs_all.append((priority, once, handler))
        self._subs_all.sort(key=lambda x: x[0], reverse=True)

    def unsubscribe(self, event_type: Type[Any], handler: Handler) -> None:
        lst = self._subs.get(event_type, [])
        self._subs[event_type] = [t for t in lst if t[2] is not handler]

    def publish(self, event: Any, *, max_chain: int = 200) -> int:
        q: Deque[Any] = deque([event])
        processed = 0

        while q:
            if processed >= max_chain:
                print(f"[EventBus] stop: reached max_chain={max_chain}")
                break

            ev = q.popleft()
            processed += 1

            subs = self._collect_handlers(type(ev)) + list(self._subs_all)

            for priority, once, handler in list(subs):
                try:
                    result = handler(ev)
                except Exception as e:
                    print("[EventBus] handler error:", repr(e))
                    continue

                if once:
                    self._remove_handler(handler)

                if result is None:
                    continue
                if isinstance(result, Iterable) and not isinstance(result, (str, bytes)):
                    for new_ev in result:
                        q.append(new_ev)
                else:
                    q.append(result)

        return processed

    def _collect_handlers(self, ev_type: Type[Any]) -> List[tuple[int, bool, Handler]]:
        result: List[tuple[int, bool, Handler]] = []
        for t in ev_type.mro():
            if t in self._subs:
                result.extend(self._subs[t])
        return result

    def _remove_handler(self, handler: Handler) -> None:
        for t, lst in self._subs.items():
            for i, (_, _, h) in enumerate(lst):
                if h is handler:
                    del lst[i]
                    return
        for i, (_, _, h) in enumerate(self._subs_all):
            if h is handler:
                del self._subs_all[i]
                return
