Refine.LocalDataSourceUI = function (controller) {
    this._controller = controller;
};

Refine.LocalDataSourceUI.prototype.attachUI = function (body) {
    this._body = body;

    this._body.html(DOM.loadHTML("local-file-system", "scripts/local-data-source-ui.html"));
    this._elmts = DOM.bind(this._body);
    var self = this;

    this._listDocuments();

    this._elmts.nextButton.html($.i18n('core-buttons/next'));
    this._elmts.nextButton.click(function (evt) {
        var e = document.getElementById("localFile");
        var optionSelIndex = e.options[e.selectedIndex].value;
        if (optionSelIndex == 0) {
            window.alert($.i18n('core-index-import/warning-data-file'));
        } else {
            self._controller._startImportJob(self._elmts.form, $.i18n('core-index-import/uploading-data'));
        }
    });

};

Refine.LocalDataSourceUI.prototype.focus = function () {
};

Refine.LocalDataSourceUI.prototype._listDocuments = function () {

    var self = this;
    Refine.wrapCSRF(function (token) {
        $.post(
            "command/core/importing-controller?" + $.param({
                "controller": "local-file-system/local-file-importing-controller",
                "subCommand": "list-documents",
                "csrf_token": token
            }),
            null,
            function (o) {
                self._renderDocuments(o);
            },
            "json"
        );
    });
};

Refine.LocalDataSourceUI.prototype._renderDocuments = function (o) {
    var self = this;

    if (!o.documents) {
        return;
    }

    document.getElementById("local-data-title").innerHTML = "Workspace files from '" + o.localPath + "'";
    this._elmts.listingContainer.empty();

    var select = $(
        '<select id="localFile" name="localFile" required><option label="Select file..."/></select>'
    ).appendTo(this._elmts.listingContainer)[0];

    var renderDocument = function (doc) {
        var option = document.createElement("option");
        option.text = doc.name;
        option.value = doc.localPath;
        select.add(option);

    };

    var docs = o.documents;
    for (var i = 0; i < docs.length; i++) {
        renderDocument(docs[i]);
    }

};

