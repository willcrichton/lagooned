define(function(require) {
    'use strict';

    return Backbone.Model.extend({
        defaults: {
            name: '',
            duration: 0
        }
    });
});
