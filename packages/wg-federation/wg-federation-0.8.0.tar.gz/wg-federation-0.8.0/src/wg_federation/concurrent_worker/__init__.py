"""
_This package can ultimately be extracted from this program to act as an external library._

This package contains an `WorkerContainer` class within a concurrent_worker module.
`WorkerContainer` aims at running tasks concurrently in a simple manner.
`WorkerContainer` is stateful, as it contains multiple `Thread` derived of registered `Worker` instances.

- `WorkerContainer` can register multiple `Worker` implementations.
Whether a `Worker` can be registered depends on several factors described below.

- Any `Worker` must be given a name, through the `name` attribute.
Any `Worker` can optionally contain contextual data, through the `context_data` attribute.

- Any `Worker` can optionally be set a `wait_seconds` attribute,
 that define the amount of time (in seconds) a `Worker` will wait before running.
`wait_date`, explained below, always takes precedence over this behavior.
`wait_seconds` will be waited before checking for any `Event` set with `wait_for`.

- Any `Worker` can optionally be set a `wait_date` attribute, that define the starting date of a `Worker`.
This uses local timezone.
Setting `wait_date` will replace `wait_seconds` entirely.

- Any `Worker` can optionally be set a `wait_for` attribute,
 a `threading.Event` that must be set before a `Worker` can run.
The default timeout is 60s.


- A `Worker`’s name attributes is checked to determine the unicity of a `Worker`.
Two `Worker`s with the same name *cannot* be both registered at the same time, but one can override the other.
You *can* register `Worker` instances from the same class multiple times, as long as their names are different.

- If `Worker` with a name `a` is registered:
 any try to register another `Worker` instance the same name `a` will result on the first `Worker` being "overriden".
An "overriden" `Worker` is simply forgotten and will never be run.
This also applies if the already registered `Worker` is still waiting (via its `wait_seconds` attribute).
However, if the already registered `Worker` is currently running:
 any try to register another `Worker` instance the same name `a` will fail with a warning raised.
This is useful to update the `context_data` of a same `Worker` while ensuring it will not run twice.

- `Worker` will be lazily un-registered when they are done running.
The un-registration happens automatically when a `WorkerContainer` instance subsequent `start_all()` calls are made.
However, calling a `WorkerContainer` instance `join_all()` will guarantee all the `Worker` instance un-registration.

- `Worker` can define a `pre_register` method, that will be run during its registration in a `WorkerContainer`.

- `WorkerContainer` can start all its registered `Worker` concurrently, by calling `start_all()`.
After `start_all()`, one can call `join_all()` to make `WorkerContainer` blocking.
`join_all()` will also guarantee that all `Worker` are properly unregistered.

Basic Usages:

```python
class MyWorker(Worker[dict]):
    _done_event: Event = None

    def __init__(
            self,
            name: str,
            context_data: _ContextDataT = None,
            wait_seconds: int = 0,
            wait_for: Event = None,
            wait_date: datetime = None,
            done_event: Event = None,
    ) -> None:
        super().__init__(name, context_data, wait_seconds, wait_date, wait_for)
        self._done_event = done_event

    def pre_register(self) -> None:
        # Dynamically set the `_must_wait` attribute, depending on contextual data
        if self._context_data and 'must_wait' in self._context_data:
            self._wait_seconds = self._context_data.get('must_wait')

    def run(self) -> None:
        print(f'Starting {self._name} for real!')
        time_taken = random.uniform(0, 3)
        time.sleep(time_taken)
        if self._done_event:
            print(f'{self._name} : signal sent {self._done_event.__class__}')
            self._done_event.set()
        print(f'{self._name} : completed in {str(time_taken)} sec')

worker_container = WorkerContainer()
worker_container.register(MyWorker(name='one'))
worker_container.register(MyWorker(name='two', context_data={'must_wait': 5}))
worker_container.register(MyWorker(name='three'))
worker_container.register(MyWorker(name='four'))
worker_container.register(MyWorker(name='five'))
worker_container.register(MyWorker(name='six'))
worker_container.start_all()
# All Worker will be started concurrently.
# Worker "two" will always be the last, because it will wait for 5 seconds before starting…
# But it will never run, see below

# This will NOT register and raise a warning: worker with the name "three" is already running.
worker_container.register(MyWorker(name='three'))

four_event = Event()
# This will work, the Worker’s name is unused
worker_container.register(MyWorker(name='four again', done_event=four_event))

# This will run after "four again"
worker_container.register(MyWorker(name='always after four', wait_for=four_event))

# This will work also because Worker "two" is currently waiting.
# This new Worker will override the one previously defined, and thus wait 7 seconds.
worker_container.register(MyWorker(name='two', context_data={'must_wait': 7}))

# Will start "four again" and "two" concurrently
# "two" will always be run last, because it will wait 7 seconds before running
# This will also un-register all the previous Worker that already run.
worker_container.start_all()

# Will wait for all the remaining Workers to finish before showing 'END OF THE PROGRAM'
# Will also un-register all remaining `Worker`.
worker_container.join_all()

print('END OF THE PROGRAM')

```
"""
