# Code and configuration guide

This repository imports the MIT-licensed code from
[GodsScion/Auto_job_applier_linkedIn](https://github.com/GodsScion/Auto_job_applier_linkedIn),
commit `e0b2401a7a7b333eab0b518e80be5285c3ee85c5`.
The upstream application, tests, and documentation were copied unchanged.
Keep `LICENSE`, `NOTICE`, and the original author notices when redistributing.

## How the code works

1. `app.py` serves the local Flask control panel and job history. `config_schema.py`
   defines the fields shown in the panel. `templates/` contains its pages.
2. The panel writes your settings into the ignored `user_config.json`.
   `config/_overrides.py` overlays those settings on the defaults in `config/*.py`.
3. `runAiBot.py` logs in through Chrome, searches and filters jobs, fills application
   questions, uploads the configured resume, and handles review/submission.
4. `modules/open_chrome.py` manages browser setup;
   `modules/clickers_and_finders.py` provides browser interactions;
   `modules/validator.py` checks configuration; `modules/helpers.py` handles shared
   utilities and logging.
5. `modules/ai/connections.py` and `prompts.py` provide optional LangChain/LangGraph
   answers using OpenAI, Gemini, or an OpenAI-compatible endpoint.
6. Application history is saved under `all excels/`, diagnostic output under `logs/`.
   `modules/updater.py` implements the upstream update facility; review updates before
   using it in this imported repository, since it contains upstream-specific behavior.

## Run locally

Requires Python 3.10+ and Chrome for the browser bot. Use a graphical desktop for
interactive browser login and prompts. The control panel and offline tests can run
without a graphical desktop.

```sh
cd /workspace/Linkedin_Job_Apply
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python app.py
```

The application prints its local control-panel address. On Windows use
`.venv\Scripts\python.exe` or `start.bat`; macOS provides `start.command` and
Linux provides `start.sh`.

On a graphical desktop, run offline tests with
`.venv/bin/python -m pytest -m "not live"`.
In this cloud workspace, use the installed virtual display:

```sh
PATH="/workspace/.local-xvfb/usr/bin:$PATH" /workspace/.local-xvfb/usr/bin/xvfb-run -a .venv/bin/python -m pytest -m "not live"
```

PyAutoGUI requires a display even for bot tests that stub Chrome.
The optional `live` test makes an external AI API call.

## Configure your own information

The shipped profile and answers are examples, not your personal information.
Replace them before running the bot. Use the control panel for its supported fields;
keep credentials and personal answers in ignored `user_config.json`, not committed
Python defaults. This application uses configuration files; simply setting similarly
named environment variables does not configure the bot.

For a review-only first run, set `settings.stop_before_submit` to `true` in
`user_config.json` (or `True` in `config/settings.py`). This option fills an
application and stops before submitting. It is different from a temporary pause.
The UI does not expose every setting.

Example override structure (merge with your other local settings):

```json
{
  "settings": {"stop_before_submit": true},
  "secrets": {"use_AI": false}
}
```

Login uses `username` and `password` when supplied, or an interactive browser session.
AI is optional: set `use_AI`, `ai_provider`, `llm_model`, `llm_api_key`, and
`llm_api_url` only if you want it. Keep keys and passwords out of Git.
See [configuration documentation](configuration.md) for allowed values and details.

## Configuration variables

These are all top-level configuration assignments in the imported source. Types are
from the shipped defaults. Exact meanings and accepted values are documented in the
linked upstream guides and comments beside each assignment.

### `personals` — [details](config-personals.md)

| Variable | Default type |
| --- | --- |
| `first_name` | `str` |
| `middle_name` | `str` |
| `last_name` | `str` |
| `phone_number` | `str` |
| `current_city` | `str` |
| `street` | `str` |
| `state` | `str` |
| `zipcode` | `str` |
| `country` | `str` |
| `ethnicity` | `str` |
| `gender` | `str` |
| `disability_status` | `str` |
| `veteran_status` | `str` |

### `questions` — [details](config-questions.md)

| Variable | Default type |
| --- | --- |
| `default_resume_path` | `str` |
| `years_of_experience` | `str` |
| `require_visa` | `str` |
| `website` | `str` |
| `linkedIn` | `str` |
| `legally_authorized` | `str` |
| `us_citizenship` | `str` |
| `desired_salary` | `int` |
| `current_ctc` | `int` |
| `notice_period` | `int` |
| `linkedin_headline` | `str` |
| `linkedin_summary` | `str` |
| `cover_letter` | `str` |
| `user_information_all` | `str` |
| `recent_employer` | `str` |
| `confidence_level` | `str` |
| `pause_before_submit` | `bool` |
| `pause_at_failed_question` | `bool` |
| `overwrite_previous_answers` | `bool` |

### `search` — [details](config-search.md)

| Variable | Default type |
| --- | --- |
| `search_terms` | `list` |
| `search_location` | `str` |
| `switch_number` | `int` |
| `randomize_search_order` | `bool` |
| `sort_by` | `str` |
| `date_posted` | `str` |
| `salary` | `str` |
| `easy_apply_only` | `bool` |
| `experience_level` | `list` |
| `job_type` | `list` |
| `on_site` | `list` |
| `companies` | `list` |
| `location` | `list` |
| `industry` | `list` |
| `job_function` | `list` |
| `job_titles` | `list` |
| `benefits` | `list` |
| `commitments` | `list` |
| `under_10_applicants` | `bool` |
| `in_your_network` | `bool` |
| `fair_chance_employer` | `bool` |
| `pause_after_filters` | `bool` |
| `about_company_bad_words` | `list` |
| `about_company_good_words` | `list` |
| `bad_words` | `list` |
| `skip_non_sponsoring_jobs` | `bool` |
| `sponsorship_offered_phrases` | `list` |
| `sponsorship_unavailable_phrases` | `list` |
| `skip_jobs_without_sponsorship` | `bool` |
| `security_clearance` | `bool` |
| `did_masters` | `bool` |
| `current_experience` | `int` |

### `secrets` — [details](config-secrets.md)

| Variable | Default type |
| --- | --- |
| `username` | `str` |
| `password` | `str` |
| `use_AI` | `bool` |
| `ai_provider` | `str` |
| `llm_model` | `str` |
| `llm_api_key` | `str` |
| `llm_api_url` | `str` |
| `llm_temperature` | `NoneType` |

### `settings` — [details](config-settings.md)

| Variable | Default type |
| --- | --- |
| `close_tabs` | `bool` |
| `follow_companies` | `bool` |
| `run_non_stop` | `bool` |
| `alternate_sortby` | `bool` |
| `cycle_date_posted` | `bool` |
| `stop_date_cycle_at_24hr` | `bool` |
| `generated_resume_path` | `str` |
| `file_name` | `str` |
| `failed_file_name` | `str` |
| `logs_folder_path` | `str` |
| `log_level` | `str` |
| `click_gap` | `int` |
| `run_in_background` | `bool` |
| `disable_extensions` | `bool` |
| `stop_before_submit` | `bool` |
| `safe_mode` | `bool` |
| `smooth_scroll` | `bool` |
| `keep_screen_awake` | `bool` |
| `auto_manage_driver` | `bool` |
| `showAiErrorAlerts` | `bool` |

