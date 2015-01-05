(function(){
    Ext.onReady(function(){
        var router = Zenoss.remote.EepRouter;

        Ext.define('eep.SettingsPanel', {
            extend: 'Ext.form.Panel',
            alias: 'widget.eep-settings-panel',
            title: 'EEP Settings',
	    id: 'eepSettingsPanel',
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
                fieldLabel: 'EEP Api Token',
                labelWidth: 200,
                name: 'eep_api_key',
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
			var panel = Ext.getCmp('eepSettingsPanel');
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

        var settings = Ext.create(eep.SettingsPanel, {
            renderTo: 'eep-settings'
        });

    }); // End Ext.onReady.
})(); // End closure.
