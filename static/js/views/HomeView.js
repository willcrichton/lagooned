define(function(require) {
    'use strict';

    var ActionsView = require('views/ActionsView'),
        LogView     = require('views/LogView');

    var template = Handlebars.compile(require('text!templates/home.html'));

    return Backbone.View.extend({
        render: function() {
            this.$el.html(template);

            // load subviews
            this.actionsView = new ActionsView().render();
            this.logView = new LogView().render();

            return this;
        }
    });
});
