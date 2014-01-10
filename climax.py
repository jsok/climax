class Task(object):
    def __init__(self, name, targets, sources):
        self.name = name
        self.targets = targets
        self.sources = sources

        self.dependencies = []

    def add_dependency(self, task_name):
        if task_name not in self.dependencies:
            self.dependencies.append(task_name)

    def __repr__(self):
        msg = "<Task name={name}, targets={targets}, sources={sources}, dependencies={dependencies}".format(
            name=self.name,
            targets=self.targets,
            sources=self.sources,
            dependencies=self.dependencies
        )
        return msg


class Climax(object):
    """
    Climax: Dependency Resolver
    """

    def __init__(self):
        self.tasks = dict()
        self.source_map = dict()

    def register_task(self, task):
        self.tasks[task.name] = task
        for target in task.targets:
            self.source_map.update({target: task.name})

    def create_graph(self):
        for name, task in self.tasks.iteritems():
            for source in task.sources:
                dependency = self.source_map.get(source, None)

                if not dependency:
                    raise Exception("Unresolved dependency %s:%s" % (name, source))
                else:
                    task.add_dependency(dependency)

    def _resolve(self, task):
        """
        Efficient resolution, but caller may encounter already resolved tasks to be returned.
        Honus is on the caller to ensure that tasks are not repeated (if they care).
        """
        for dependency in task.dependencies:
            for dep in self.resolve(self.tasks[dependency]):
                yield dep
        yield task

    def resolve(self, task):
        if isinstance(task, str):
            task = self.tasks[task]

        resolved = []
        self.resolve_full(task, resolved, [])
        return resolved

    def resolve_full(self, task, resolved, unresolved):
        unresolved.append(task)
        for dependency in task.dependencies:
            dependency = self.tasks[dependency]
            if dependency not in resolved:
                if dependency in unresolved:
                    raise Exception('Circular reference detected: %s -> %s' % (task.name, dependency.name))
                self.resolve_full(dependency, resolved, unresolved)
        resolved.append(task)
        unresolved.remove(task)


if __name__ == "__main__":
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

