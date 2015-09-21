(function () {

    angular.module('baseApp')
        .controller('mainController', ['$mdSidenav', 'logger', mainController]);

    function mainController($mdSidenav, $logger) {
        var self = this;

        self.focus = 'page1';

        self.activate = function (element) {
            self.focus = element;
        };

        self.toggle = function () {
            $mdSidenav('left').toggle();
        };
    }
})();
