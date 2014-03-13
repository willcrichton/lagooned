define(function(require) {
    'use strict';

    return Backbone.Model.extend({
        className: 'User',
        defaults: {
            name: '',
            login: false,
            hunger: 0,
            log: [],
            items: {}
        }
    });
});
