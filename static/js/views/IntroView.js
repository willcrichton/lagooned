define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/intro.html'));

    return Backbone.View.extend({
        render: function() {
            this.$el.html(template);
            return this;
        }
    });
});
