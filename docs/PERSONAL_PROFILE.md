# CV profile and India search

The uploaded CV has been configured in this cloud checkout using the ignored
`user_config.json`. Its PDF is stored at
`all resumes/default/Ujjwal_Singh_Resume.pdf` (also ignored). Neither file is
included in Git. A fresh clone must receive these local files separately.

The profile includes the CV's name, contact details, Noida location, employer,
B.Tech education in its background context, performance testing skills, and the
stated 5.6 years of experience. Skill-specific years are not invented. The
existing integer search experience filter uses 5 completed years; free-text
application answers retain the CV's exact `5.6` value.

Search terms target performance testing, load testing, JMeter, LoadRunner and
BlazeMeter roles. The search country is India with no city allowlist or work
setting restriction. `excluded_locations` is editable in the Search tab and
defaults to Chennai and Madras. Matching uses whole city phrases, ignoring case.
Jobs listing either city are skipped, including remote or multi-city listings.
Unknown job-card locations are skipped while exclusions are configured. This
filter uses the listing's location, not every city mentioned in its description.

Confirmed compensation, notice period and LinkedIn URL are stored in the local
profile. The expected CTC range is retained in the background context; forms
requiring one numeric value use its upper bound. These personal values are not
included in Git. Salary and notice fields support JSON `null` if cleared later.
Visa, work authorization, citizenship, portfolio URL and confidence rating remain
blank until provided. Contact email is separate from the LinkedIn login.

AI is disabled in the local profile. `stop_before_submit` is enabled, so a run
fills an application and discards it at review rather than submitting it. No
LinkedIn applications were run during this update.

Local profile validation and the offline tests passed. To test on this cloud image:

```sh
cd /workspace/Linkedin_Job_Apply
PATH="/workspace/.local-xvfb/usr/bin:$PATH" /workspace/.local-xvfb/usr/bin/xvfb-run -a .venv/bin/python -m pytest -m "not live"
```
