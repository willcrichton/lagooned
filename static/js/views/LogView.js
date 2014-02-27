define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/log.html'));

    return Backbone.View.extend({
        el: '#log',
        render: function() {
            this.$el.html(template);
            return this;
        }
    });
});
