define(function(require) {
    'use strict';

    var ActionsView   = require('views/ActionsView'),
        LogView       = require('views/LogView'),
        ItemsView     = require('views/ItemsView'),
        BuildingsView = require('views/BuildingsView');

    var template = Handlebars.compile(require('text!templates/home.html'));

    return Backbone.View.extend({
        initialize: function() {
            this.listenTo(GAME.me, 'change', function() {
                var location = GAME.me.get('location');
                if (location == '') return;

                $('#background').attr('class', location);
            });
        },
        
        render: function() {
            this.$el.html(template);

            // load subviews
            this.actionsView = new ActionsView().render();
            this.logView = new LogView().render();
            this.itemsView = new ItemsView().render();
            this.buildingsView = new BuildingsView().render();

            // set height of bg to viewport size
            this.$('#background').css('height', window.innerHeight);

            return this;
        }
    });
});
