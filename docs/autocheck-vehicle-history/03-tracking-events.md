# События аналитики: «История авто» (Autocheck)

**Статус:** предложение v0.1.0, ещё не внесено в план трекинга
**Дата:** 04.11.2026
**Связано с:** `02-prd-istoriya-avto.md`, требование R6

> В репозитории нет `.telemetry/tracking-plan.yaml`, поэтому формальный дельта-апдейт плана не выполнен. Этот документ содержит готовый дизайн событий. Чтобы завести план и перенести события в него, запустите скилл **product-tracking-design-tracking-plan** («design tracking plan»), затем **product-tracking-instrument-new-feature** для этой фичи.

## Принципы

- Формат имён `object.action`, snake_case, глагол в прошедшем времени. Если в приложении уже принят другой формат (например `Object Verb`), переименовать по действующему соглашению, не смешивать.
- Отслеживаем результат, а не клик: `report_purchased`, а не `button_clicked`.
- Без персональных данных в свойствах: нет VIN, госномера, номера техпаспорта, ИИН. Сделка и отчёт только по внутренним идентификаторам.
- Четыре события на запуск. Остальное через свойства.

## События

### 1. `vehicle_check.preview_completed`

Превью по авто получено и показано пользователю, либо запрос завершился ошибкой. Категория: core_value. Частота: одно на открытие блока без кэша.

| Свойство | Тип | Обязательное | Значения / смысл |
|---|---|---|---|
| `entry_point` | string | да | `deal_buyer`, `deal_seller`, `miniapp` |
| `identifier_type` | string | да | `vin`, `grnz` |
| `result` | string | да | `success`, `not_found`, `failed` |
| `error_code` | string | нет | `srts_required`, `srts_mismatch`, `grnz_not_supported`, `source_unavailable`, `not_found` |
| `owners_count` | integer | нет | Число владельцев из превью |
| `has_restriction` | boolean | нет | Признак обременения |
| `has_coowners` | boolean | нет | Признак совладельцев |
| `model_mismatch` | boolean | нет | Заявленные продавцом модель или год не совпали с превью (только в сделке) |
| `from_cache` | boolean | да | Превью отдано из кэша |
| `latency_ms` | integer | да | Время ответа бэкенда |
| `deal_id` | string | нет | Внутренний идентификатор сделки |

### 2. `vehicle_check.report_purchased`

Полный отчёт куплен, ссылка получена, проверка списана. Категория: core_value / billing. Частота: не больше одного на сделку, по клиентам миниаппа без ограничений.

| Свойство | Тип | Обязательное | Значения / смысл |
|---|---|---|---|
| `entry_point` | string | да | `deal_buyer`, `miniapp` |
| `payer` | string | да | `retail_bu`, `client`, `partner` (на будущее после переговоров) |
| `price_kzt` | integer | да | Цена для плательщика. Для `retail_bu` оптовая цена, для `client` розничная |
| `price_variant` | string | нет | Вариант A/B цены в миниаппе |
| `seconds_since_preview` | integer | нет | Время от превью до покупки |
| `report_id` | string | да | Идентификатор отчёта Autocheck для сверки с партнёром |
| `deal_id` | string | нет | Внутренний идентификатор сделки |

### 3. `vehicle_check.report_purchase_failed`

Покупка не состоялась. Категория: error. Частота: редкая.

| Свойство | Тип | Обязательное | Значения / смысл |
|---|---|---|---|
| `entry_point` | string | да | `deal_buyer`, `miniapp` |
| `payer` | string | да | `retail_bu`, `client` |
| `reason` | string | да | `balance_exhausted`, `limit_reached`, `payment_declined`, `token_not_found`, `partner_error` |
| `deal_id` | string | нет | Внутренний идентификатор сделки |

### 4. `vehicle_check.report_opened`

Пользователь открыл страницу отчёта в webview. Категория: engagement. Частота: несколько на отчёт.

| Свойство | Тип | Обязательное | Значения / смысл |
|---|---|---|---|
| `entry_point` | string | да | `deal_buyer`, `deal_seller`, `miniapp`, `profile_reports` |
| `payer` | string | да | `retail_bu`, `client` |
| `first_open` | boolean | да | Первое открытие после покупки |
| `report_id` | string | да | Идентификатор отчёта |

## Изменение существующих событий сделки

На события завершения и отмены сделки «Переоформление авто» (имена уточнить в текущем плане) добавить необязательное свойство:

| Свойство | Тип | Значения |
|---|---|---|
| `vehicle_check_level` | string | `none`, `preview`, `full_report` |

Это позволяет сравнить долю возвратов и отмен по сделкам с проверкой и без. Свойство необязательное, изменение не ломающее.

## Где внедрять

| Событие | Где | Примечание |
|---|---|---|
| `preview_completed` | Бэкенд-прокси, обработчик превью, после ответа Autocheck или кэша | Серверное событие, чтобы не терять ошибки до отрисовки |
| `report_purchased` | Бэкенд-прокси, обработчик решения о покупке, после получения ссылки `next` | Серверное событие |
| `report_purchase_failed` | Бэкенд-прокси, ветки 402, лимита, отказа платежа, 404 по токену | Серверное событие |
| `report_opened` | Мобильный клиент, открытие webview отчёта | Клиентское событие |
| `vehicle_check_level` | Там, где сейчас отправляются события завершения и отмены сделки | Свойство берётся из состояния сделки |

Identify и group не меняются: пользователь уже идентифицирован в приложении, группового уровня у B2C-сделки нет.

## Воронки для дашборда

1. Сделка: экран сделки → `preview_completed` (`success`) → `report_purchased` → перевод денег → завершение сделки, срез по `vehicle_check_level`.
2. Миниапп: ввод идентификатора → `preview_completed` → `report_purchased` (`payer = client`) → `report_opened`, срез по `price_variant`.
3. Надёжность: доля `result = failed` и `report_purchase_failed` по `reason`, p95 `latency_ms`.

## Версия

Предлагаемая запись в changelog плана трекинга после его создания:

```
## [1.1.0] - 2026-11-04
### Added
- vehicle_check.preview_completed, vehicle_check.report_purchased,
  vehicle_check.report_purchase_failed, vehicle_check.report_opened
### Changed
- события завершения и отмены сделки: добавлено необязательное свойство vehicle_check_level
```
