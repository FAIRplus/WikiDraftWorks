Refine.LocalFileSystemImportingController = function (createProjectUI) {
    this._createProjectUI = createProjectUI;

    this._fileSelectionPanel = createProjectUI.addCustomPanel();
    this._parsingPanel = createProjectUI.addCustomPanel();

    createProjectUI.addSourceSelectionUI({
        label: "Workspace Data",
        id: "local-source",
        ui: new Refine.LocalDataSourceUI(this)
    });
};
Refine.CreateProjectUI.controllers.push(Refine.LocalFileSystemImportingController);

Refine.LocalFileSystemImportingController.prototype = Refine.DefaultImportingController.prototype;

Refine.LocalFileSystemImportingController.prototype._startImportJob = function (form, progressMessage, callback) {
    var self = this;

    Refine.wrapCSRF(function (token) {
        $.post(
            "command/core/create-importing-job",
            {csrf_token: token},
            function (data) {
                var jobID = self._jobID = data.jobID;

                form.attr("method", "post")
                    .attr("accept-charset", "UTF-8")
                    .attr("target", "create-project-iframe")
                    .attr("action", "command/core/importing-controller?" + $.param({
                        "controller": "local-file-system/local-file-importing-controller",
                        "jobID": jobID,
                        "subCommand": "load-raw-data",
                        "csrf_token": token
                    }));
                form[0].submit();

                var start = new Date();
                var timerID = window.setInterval(
                    function () {
                        self._createProjectUI.pollImportJob(
                            start, jobID, timerID,
                            function (job) {
                                return job.config.hasData;
                            },
                            function (jobID, job) {
                                self._job = job;
                                self._onImportJobReady();
                                if (callback) {
                                    callback(jobID, job);
                                }
                            },
                            function (job) {
                                alert(job.config.error + '\n' + job.config.errorDetails);
                                self._startOver();
                            }
                        );
                    },
                    1000
                );
                self._createProjectUI.showImportProgressPanel(progressMessage, function () {
                    // stop the iframe
                    $('#create-project-iframe')[0].contentWindow.stop();

                    // stop the timed polling
                    window.clearInterval(timerID);

                    // explicitly cancel the import job
                    Refine.wrapCSRF(function (token) {
                        $.post("command/core/cancel-importing-job?" + $.param({"jobID": jobID}),
                            {csrf_token: token});
                    });

                });
            },
            "json"
        );
    });
};
