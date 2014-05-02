define(function(require) {
    'use strict';

    var template = Handlebars.compile(require('text!templates/intro.html'));

    return Backbone.View.extend({
        render: function() {
            setTimeout(_.bind(function() {
                this.router.navigate('home', {trigger: true});
            }, this), 0);

            this.$el.html(template);
            return this;
        }
    });
});
