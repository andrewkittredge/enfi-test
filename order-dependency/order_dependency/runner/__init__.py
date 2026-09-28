"""Running an experiment: its settings, its execution, and its record.

* ``llm_config.LLMConfig`` - model/backend settings; ``LLMConfig.answerer`` builds the backend.
* ``run_experiment`` - ``plan`` the prompts and ``run_experiment`` them concurrently.
* ``preflight_error.PreflightError`` - raised when the very first request fails.
* ``experiment_run.ExperimentRun`` - the self-contained record a run produces.
"""
