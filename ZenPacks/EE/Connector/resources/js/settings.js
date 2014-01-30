(function(){
    Ext.onReady(function(){
        var router = Zenoss.remote.EeRouter;

        Ext.define('ee.SettingsPanel', {
            extend: 'Ext.form.Panel',
            alias: 'widget.ee-settings-panel',
            title: 'EE Settings',
	    id: 'eeSettingsPanel',
            defaults: {
                listeners: {
                    specialkey: function(field, event) {
                        if (event.getKey() == event.ENTER) {
                           field.up('form').submit();
                        }
                    }
                }
            },
            items: [{
                fieldLabel: 'EE Api Token',
                labelWidth: 200,
                name: 'ee_api_key',
                xtype: 'textfield'
            }],
            dockedItems: [{
                dock: 'bottom',
                xtype: 'toolbar',
                ui: 'footer',
                items: [{
		    xtype: 'button',
                    text: 'Save',
                    handler: function() {
			var panel = Ext.getCmp('eeSettingsPanel');
                        panel.submit();
                    }
                }]
            }],
            onRender: function() {
                this.callParent(arguments);
                this.load();
            },
            load: function() {
                router.loadSettings({}, function(result) {
                    this.getForm().setValues(result.data);
                }, this);
            },
            submit: function() {
                router.submitSettings(this.getForm().getValues());
            }
        });

        var settings = Ext.create(ee.SettingsPanel, {
            renderTo: 'ee-settings'
        });

    }); // End Ext.onReady.
})(); // End closure.
