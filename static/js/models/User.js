define(function(require) {
    'use strict';

    return Backbone.Model.extend({
        className: 'User',
        defaults: {
            name: '',
            login: false,
            food: 0,
            log: [],
            items: {}
        }
    });
});
