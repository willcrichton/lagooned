define(function(require) {
    'use strict';

    return Backbone.Model.extend({
        defaults: {
            name: '',
            label: '',
            duration: 0
        }
    });
});
