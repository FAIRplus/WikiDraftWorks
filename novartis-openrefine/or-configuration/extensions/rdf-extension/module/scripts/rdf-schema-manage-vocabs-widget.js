function ManageVocabsWidget(manager){
	this._prefixesManager = manager;
}

ManageVocabsWidget.prototype.show = function(){
	var self = this;
	
    var dialog = $(DOM.loadHTML("rdf-extension", "scripts/dialogs/rdf-schema-manage-vocabs-widget.html"));
    self._level = DialogSystem.showDialog(dialog);
    self._elmts = DOM.bind(dialog);
    
    self._elmts.dialogHeader.html($.i18n('rdf-ext-vocab/header'));
    self._elmts.addPrefixBtn.html($.i18n('rdf-ext-buttons/add-prefix'));
    self._elmts.okButton.html($.i18n('rdf-ext-buttons/ok'));
    self._elmts.cancelButton.html($.i18n('rdf-ext-buttons/cancel'));    
    
    self._elmts.cancelButton.click(function() { self._dismiss(); });
    
	self._elmts.addPrefixBtn.click(function(e){
		e.preventDefault();
		self._prefixesManager._addPrefix(
				false,
				false,
				function(){
					self.renderBody();
					}
				);
	});

    
    self.renderBody();
	
	self._elmts.okButton.click(function() {
    	self._prefixesManager._showPrefixes();
		self._dismiss();
	});
	
};

ManageVocabsWidget.prototype.renderBody = function(){
	var self = this;
	
	var table = self._elmts.prefixesTable;
	table.empty();
    table.append($('<tr>').addClass('rdf-table-even')
    		.append($('<th/>').text($.i18n('rdf-ext-vocab/prefix')))
    		.append($('<th/>').text($.i18n('rdf-ext-vocab/uri')))
    		.append($('<th/>').text($.i18n('rdf-ext-vocab/delete')))
    		.append($('<th/>').text($.i18n('rdf-ext-vocab/refresh')))
    		);
    
	var getDeleteHandler = function(name){
		return function(e){
			e.preventDefault();
			dismissBusy = DialogSystem.showBusy($.i18n('rdf-ext-vocab/deleting-pref')+' ' + name);
			Refine.wrapCSRF(function(token) {
			    $.post(
					'command/rdf-extension/remove-prefix',
					{
						'name':name,
						'project':theProject.id,
						'csrf_token': token,
					},
					function(data)
					{
						dismissBusy();
						if(data.code === 'error'){
							//TODO
							console.log($.i18n('rdf-ext-vocab/error-deleting'));
						}else{
							self._prefixesManager._removePrefix(name);
							self.renderBody();
						}
					}
				);
			});
    	}; 
    };
    
    var getRefreshHandler = function(name,uri){
    	return function(e){
    		e.preventDefault();
    		if (window.confirm($.i18n('rdf-ext-vocab/desc-one')+" \"" + uri + 
    				"\" \n"+$.i18n('rdf-ext-vocab/desc-two'))) 
    		{
    			
    			dismissBusy = DialogSystem.showBusy($.i18n('rdf-ext-vocab/refresh-pref')+' ' + name);
    			Refine.wrapCSRF(function(token) {
    			    $.post('command/rdf-extension/refresh-prefix',
    					{
    						'name':name,
    						'uri':uri,
    						'project':theProject.id,
    						'csrf_token': token
    					},
						function(data) {
							dismissBusy();
		    				if(data.code==='error'){
		    					alert($.i18n('rdf-ext-vocab/alert-wrong')+': ' + data.messge);
		    				}
						});
    		        });
    		    }
    	    };
    };

	for(var i = 0; i< self._prefixesManager._prefixes.length; i++){
		var name = self._prefixesManager._prefixes[i].name;
		var uri = self._prefixesManager._prefixes[i].uri;
		var delete_handle = $('<a/>').text($.i18n('rdf-ext-vocab/delete')).attr('href','#').click(getDeleteHandler(name));
		var refresh_handle = $('<a/>').text($.i18n('rdf-ext-vocab/refresh')).attr('href','#').click(getRefreshHandler(name,uri));
		var tr = $('<tr/>').addClass(i%2==1?'rdf-table-even':'rdf-table-odd')
		.append($('<td>').text(self._prefixesManager._prefixes[i].name))
		.append($('<td>').text(self._prefixesManager._prefixes[i].uri))
		.append($('<td>').html(delete_handle))
		.append($('<td>').html(refresh_handle));
		table.append(tr);
	}

};


ManageVocabsWidget.prototype._dismiss = function() {
	DialogSystem.dismissUntil(this._level - 1);
};
