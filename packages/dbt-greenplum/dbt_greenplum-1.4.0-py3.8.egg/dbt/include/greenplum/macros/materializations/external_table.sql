{% materialization external_table, adapter='greenplum' %}

  {{ log('identifier: ' + identifier|string, info=True) }}
  {{ log('schema: ' + schema|string, info=True) }}
  {{ log('this: ' + this|string, info=True) }}

  {# {%- set existing_relation = adapter.get_relation(this, identifier=identifier, schema=schema) -%} #}
  {{ log('1', info=True) }}
  {%- set target_relation = api.Relation.create(
        identifier=identifier, schema=schema, database=database,
        type='external_table') -%}

  {{ log('2', info=True) }}
  {%- set intermediate_relation =  make_intermediate_relation(target_relation) -%}
  -- the intermediate_relation should not already exist in the database; get_relation
  -- will return None in that case. Otherwise, we get a relation that we can drop
  -- later, before we try to use this name for the current operation
  {{ log('3', info=True) }}
  {%- set preexisting_intermediate_relation = load_cached_relation(intermediate_relation) -%}
  /*
      See ../view/view.sql for more information about this relation.
  */
  {{ log('4', info=True) }}
  {%- set backup_relation_type = 'external_table' if existing_relation is none else existing_relation.type -%}

  {{ log('5', info=True) }}
  {%- set backup_relation = make_backup_relation(target_relation, backup_relation_type) -%}
  -- as above, the backup_relation should not already exist

  {{ log('6', info=True) }}
  {%- set preexisting_backup_relation = load_cached_relation(backup_relation) -%}

  -- drop the temp relations if they exist already in the database
  {{ log('7', info=True) }}
  {{ drop_relation_if_exists(preexisting_intermediate_relation) }}

  {{ log('9', info=True) }}
  {{ drop_relation_if_exists(preexisting_backup_relation) }}

  {{ log('10', info=True) }}
  {{ run_hooks(pre_hooks, inside_transaction=False) }}

  -- `BEGIN` happens here:
  {{ log('10', info=True) }}
  {{ run_hooks(pre_hooks, inside_transaction=True) }}

  -- build model
  {{ log('11', info=True) }}
  {% call statement('main') -%}
    {{ get_create_external_table_as_sql(False, intermediate_relation, sql) }}
  {%- endcall %}

  -- cleanup
  {{ log('12', info=True) }}
  {% if existing_relation is not none %}
      {{ adapter.rename_relation(existing_relation, backup_relation) }}
  {% endif %}

  {{ log('13', info=True) }}
  {{ adapter.rename_relation(intermediate_relation, target_relation) }}

  {{ log('14', info=True) }}
  {{ run_hooks(post_hooks, inside_transaction=True) }}

  {{ log('15', info=True) }}
  {% do persist_docs(target_relation, model) %}

  -- `COMMIT` happens here
  {{ log('16', info=True) }}
  {{ adapter.commit() }}

  -- finally, drop the existing/backup relation after the commit
  {{ log('17', info=True) }}
  {{ drop_relation_if_exists(backup_relation) }}

  {{ log('18', info=True) }}
  {{ run_hooks(post_hooks, inside_transaction=False) }}

  {{ log('19', info=True) }}
  {{ return({'relations': [target_relation]}) }}

{% endmaterialization %}