{% macro get_create_external_table_as_sql(temporary, relation, sql) -%}
  {{ adapter.dispatch('get_create_table_as_sql', 'dbt')(temporary, relation, sql) }}
{%- endmacro %}


{% macro default__get_create_external_table_as_sql(temporary, relation, sql) -%}
  {{ return(create_table_as(temporary, relation, sql)) }}
{% endmacro %}


{% macro default__create_external_table_as(temporary, relation, sql) -%}
  {%- set sql_header = config.get('sql_header', none) -%}

  {{ sql_header if sql_header is not none }}

  create {% if temporary: -%}temporary{%- endif %} table
    {{ relation.include(database=(not temporary), schema=(not temporary)) }}
  as (
    {{ sql }}
  );
{%- endmacro %}


{% macro greenplum__external_create_table_as(temporary, relation, sql) -%}
  {%- set sql_header = config.get('sql_header', none) -%}

  {%- set type = config.get('type', default=false) -%}

  {%- set locations = config.get('locations', default=false) -%}
  {%- set web = config.get('web', default=false) -%}
  {%- set web = config.get('web', default=false) -%}
  {%- set format = config.get('format', none) -%}
  {%- set format_options = config.get('format_options', none) -%}
  {%- set encoding = config.get('encoding', none) -%}
  {%- set segment_reject_limit = config.get('segment_reject_limit', none) -%}
  {%- set segment_reject_limit_type = config.get('segment_reject_limit', none) -%}
  {%- set log_errors = config.get('log_errors', none) -%}
  {%- set distributed_randomly = config.get('distributed_randomly', default=false) -%}
  {%- set distributed_by = config.get('distributed_by', none) -%}
  {%- set execute_command = config.get('execute_command', none) -%}
  {%- set on_master = config.get('on_master', none) -%}
  {%- set on_all = config.get('on_all', none) -%}

  {{ sql_header if sql_header is not none }}


  create external table {{ 'web' if web else '' }} {{ relation }}
  (sql)
  {% if execute_command is none %}
      location (
      {% for location in locations %}
        {{ location }}
        {%- if not loop.last %},{% endif -%}
      {% endfor %}
      )
  {% else %}
      execute {{ execute_command }}
  {% endif %}
  FORMAT {{ format }} {{ '(' + format_options + ')' if format_options else '' }}
  {{ encoding if encoding is not none '' }}
  {{ segment_reject_limit if segment_reject_limit else '' }}



{%- endmacro %}


{% macro create_readable_external_table_as() %}

{% endmacro %}