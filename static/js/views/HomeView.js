define(function(require) {
    'use strict';

    var ActionsView = require('views/ActionsView'),
        LogView     = require('views/LogView'),
        ItemsView   = require('views/ItemsView'),
        StatsView   = require('views/StatsView');

    var template = Handlebars.compile(require('text!templates/home.html'));

    return Backbone.View.extend({
        render: function() {
            this.$el.html(template);

            // load subviews
            this.actionsView = new ActionsView().render();
            this.logView = new LogView().render();
            this.itemsView = new ItemsView().render();
            this.statsView = new StatsView().render();

            return this;
        }
    });
});
