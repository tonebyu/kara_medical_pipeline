select
  distinct date::date as date
from {{ ref('stg_telegram_messages') }}
