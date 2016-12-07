# collectd-clickhouse
clickhouse plugin written in Python

Configure this plugin based on collectd.conf parts.

Example configuration:
```
<LoadPlugin python>
       Globals true
</LoadPlugin>

TypesDB "/usr/local/lib/collectd/python/clickhouse_types.db"

<Plugin python>
    ModulePath "/usr/local/lib/collectd/python/"
    LogTraces true
    Interactive false
    Import "clickhouse"
    <Module clickhouse>
        URL "http://localhost:8123/"
        User "default"
        Password ""
    </Module>
</Plugin>
```
