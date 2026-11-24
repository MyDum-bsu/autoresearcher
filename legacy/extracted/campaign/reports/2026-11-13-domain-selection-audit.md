# Phase C terminal audit: partial engineering disposition

The final broad text-hygiene audit exited 1. Its six findings are missing final LF characters in the raw `pdftotext -layout` outputs `research/sources/A2.txt`, `A3.txt`, `A4.txt`, `BT04.txt`, `GTW20.txt` and `GTW25.txt`. The failed observation is preserved in `research/phase-c-terminal-verification.json`; it is not reported as green. No rerun, newline normalization, source replacement, hash amendment or frozen-pool change followed this failure.

The four requested research artifacts exist and were independently checked earlier in this session: `research/domain-packet.md`, `research/question.md`, `research/closest-results.md`, `research/resource-manifest.json`. That narrower packet-integrity check returned exit 0, checking 75 common-file hashes, six original/copy PDF identities, 21 literal PDF-page anchors and the main packet's authored-text hygiene. Three style diagnostics returned exit 0. Evidence: `research/phase-c-verification.json`, `research/phase-c-style.txt`. These observations are distinct from the later failed audit and are not substituted for it.

## What the final failure means

The broad audit applied a final-LF requirement to converter-produced raw text as well as authored documents. It found a real byte-level property of those converter outputs. All six were already frozen as exact extraction products. They are auxiliary page-extraction evidence, not executable scientific results; the original PDFs, selected-page context, inspected renderings and literal page anchors remain available and hash-bound. The earlier successful comparison against the original PDF bytes and page excerpt membership is unaffected. The final audit produced no evidence of source drift, missing requested packet, wrong branch, tracked-file changes or a failed mathematical inference.

This worker does not silently waive the audit or change the validator to make it pass. Phase C's engineering handoff is therefore **partial**, with this audit finding retained. The preceding phase report and Russian briefing were written before the final audit; read them together with this addendum, not as a claim that every later check passed. `research/phase-c-delivery.json` is the inventory as captured by the failed audit and keeps its historical `safeToContinue=false`; this addendum and the terminal worker result supply the subsequent scoped continuation decision without rewriting that record.

## Scoped continuation decision

`safeToContinue=true` for D1/D2 scientific investigation: the owner-defined meaning is sufficient anchored material for bounded honest investigation. The observed lack of final LF in unchanged raw extracts does not withhold a model premise, alter the question/source/tool pool or block candidate-specific rational certificate checks. No claim that the terminal hygiene audit passed is made. A coordinator may instead pause for an explicit disposition of that engineering finding; it must not normalize these frozen files silently or rerun completed research.

The selected question remains `correlated-continuation-compatibility-v1`, a boundary/reconstruction objective with novelty unestablished. Final common-manifest SHA-256 remains `1ff15746b0a2c8c47499cefdeca9dc2fc6b95c92ef536ce2e9259d7b542373d8`. Question SHA-256 remains `6e6bbaff0d752c3bfe7e2f9ee78b3135e689e437e012730f4c482c3a31f786dc`. No exact new construction, general proof, human semantic approval or scientific attestation is claimed.

The other observed failure, ambiguous unique-phrase extraction, is preserved separately in `research/sources/preparation-observation.json`; it was not retried. Terminal scope decisions are accounting, not a new source, mathematical checker or permission to enrich only one public attempt's pool.

## Сообщение владельцу

Финальный аудит завершился с exit 1: в шести необработанных TXT-выгрузках PDF нет завершающего LF. Ошибка сохранена; повторов и изменения замороженных файлов не было. Поэтому инженерный итог этой фазы отмечен как частичный, а не полностью зелёный.

Исследовательский пакет подготовлен: один точный вопрос, шесть исходных PDF с происхождением, сравнение ближайших результатов и общий набор источников/инструментов для обеих попыток. Ранее отдельно прошли проверка идентичностей и 21 PDF-якоря, а также проверка оформления четырёх основных файлов. Новизна и новая теорема не заявлены. Рекомендация — продолжить ограниченные D1/D2 с неизменным manifest, сохранив замечание аудита отдельно: отсутствие LF в сыром выводе конвертера не лишает исследование источников или точного маршрута проверки.
