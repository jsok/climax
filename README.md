Climax - Dependency Resolution
==============================

Usage
-----

```python
    from climax import Climax, Task

    task_main = Task('main.c', ['main.obj'], ['foo.obj', 'bar.obj'])
    task_foo = Task('foo.c', ['foo.obj'], ['bar.obj', 'baz.obj'])
    task_bar = Task('bar.c', ['bar.obj'], [])
    task_baz = Task('baz.c', ['baz.obj'], [])

    d = Climax()
    d.register_task(task_main)
    d.register_task(task_foo)
    d.register_task(task_bar)
    d.register_task(task_baz)

    for task in d.resolve(task_main):
        print task
```