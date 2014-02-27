define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/actions.html'));

    return Backbone.View.extend({
        el: '#actions',
        render: function() {
            this.$el.html(template);
            return this;
        }
    });
});
