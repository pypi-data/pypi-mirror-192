# easyapi-django

A multitenant muiltidatabase MySql router for Django

## Install

```
pip install tenant-django
```

## Add database router to Django settings

```
DATABASE_ROUTERS = ['tenant.DBRouter']
```

## Set tenant

```
from tenant import set_tenant

set_tenant(identifier)
```
