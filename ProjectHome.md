This app allow you keep a history (aka copies of previous records in the database) for Django Models.

You should be able to plug this into your project, register models on which you want history to be kept and the rest should just work(tm).

Currently this is a proof of concept. Which proofs we can automatically creating normally behaving extra Django models in-place besides your existing models. Therefor we don't need to pickle objects, and we can use every bit of the mighty queryset power directly on it.

Pro's: No pickling!! therefor; the history will not break completely when you modify your models, there's no magic trickery behind the scenes to recreate objects, FAST changesets/diff and other operations should be as fast as normal database access and no endian madness when migrating platforms.

Con's: Double the trouble of schema changes. You'll need to apply the same changes you make to your normal tables in the database, to your history tables as well. (Actually you only need to apply the changes that add to the tables, such as ALTER TABLE ADD and ALTER TABLE SET VARCHAR(bigger). You won't need to remove fields if you remove them from your models)

I'll develop features for it depending on how much interest there is for a Django History/VersionControl applications based on this approach.

Download by cloning the mercurial repository and install as normal Django application. You can also see the examples/ directory for some usage examples and test cases.