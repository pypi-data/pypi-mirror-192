from django.db import models

class Procedure(models.Model):
    parent = models.ForeignKey('self', related_name='children', null=True, on_delete=models.CASCADE)

    parameters = models.JSONField(default=dict)
    results = models.JSONField(default=dict)

    name = models.TextField(default=str)
    environ = models.JSONField(default=dict)
    executed = models.BooleanField(default=False)
    logs = models.TextField()

    def __str__(self):
        return self.name

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return False

    def sub(self, name):
        (sub_procedure, _) = self.children.get_or_create(name=name)
        return sub_procedure

    def run(self, task, *args, **kwargs):
        return task(*args, **kwargs)

    def get(self, variable, default=None):
        return self.environ.get(variable, default)

    def set(self, variable, value, commit=True):
        self.environ[variable] = value
        if commit:
            self.save(update_fields=['variable'])

    def log(self, text, commit=True):
        self.logs += text
        if commit:
            self.save(update_fields=['logs'])
