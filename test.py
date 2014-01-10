from unittest import TestCase, skip
from nose.tools import *

from climax import Climax, Task


class DependsTestCase(TestCase):
    def setUp(self):
        self.task_a = Task('A', ['foo', 'bar'], [])
        self.task_b = Task('B', ['dog'], ['bar'])
        self.task_c = Task('C', ['cat'], ['dog'])

    def test_register_tasks(self):
        d = Climax()

        d.register_task(self.task_a)
        d.register_task(self.task_b)
        d.register_task(self.task_c)

        assert_equal(len(d.tasks), 3)

    def test_register_tasks(self):
        d = Climax()

        d.register_task(self.task_a)
        d.register_task(self.task_b)
        d.register_task(self.task_c)

        d.create_graph()

        print
        for task in d.resolve(self.task_c):
            print task

    def test_example2(self):
        task_main = Task('main.c', ['main.obj'], ['foo.obj', 'bar.obj'])
        task_foo = Task('foo.c', ['foo.obj'], ['bar.obj', 'baz.obj'])
        task_bar = Task('bar.c', ['bar.obj'], [])
        task_baz = Task('baz.c', ['baz.obj'], [])

        d = Climax()
        d.register_task(task_main)
        d.register_task(task_foo)
        d.register_task(task_bar)
        d.register_task(task_baz)

        d.create_graph()

        print
        for task in d.resolve(task_main):
            print task

    @raises(Exception)
    def test_example_circular_dependency(self):
        task_a = Task('A', ['dog'], ['bar'])
        task_b = Task('B', ['bar'], ['dog'])

        d = Climax()
        d.register_task(task_a)
        d.register_task(task_b)
        d.create_graph()
        d.resolve(task_b)
