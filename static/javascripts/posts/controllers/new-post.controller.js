/**
* NewPostController
* @namespace lostitems.posts.controllers
*/
(function () {
  'use strict';

  angular
    .module('lostitems.posts.controllers')
    .controller('NewPostController', NewPostController);

  NewPostController.$inject = ['$rootScope', '$scope', 'Authentication', 'Snackbar', 'Posts', 'Upload'];

  /**
  * @namespace NewPostController
  */
  function NewPostController($rootScope, $scope, Authentication, Snackbar, Posts, Upload) {
    var vm = this;

    vm.submit = submit;

    /**
    * @name submit
    * @desc Create a new Post
    * @memberOf lostitems.posts.controllers.NewPostController
    */
    function submit() {

      Upload.upload({
                  url: '/api/v1/posts/',
                  data: {file: vm.datafile, 'content': vm.content}
              }).then(createPostSuccessFn
              ,createPostErrorFn
              , function (evt) {
                  var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                  console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
              });


      //Posts.create(vm.content, vm.datafile).then(createPostSuccessFn, createPostErrorFn);


      /**
      * @name createPostSuccessFn
      * @desc Show snackbar with success message
      */
      function createPostSuccessFn(data, status, headers, config) {
        //Hack: The url file is returning with the "/api/v1/posts/" string wrongly. Issue with the django rest framework
        var datafile =  data.data.datafile.replace(data.config.url, "/");
      $rootScope.$broadcast('post.created', {
        content: vm.content,
        datafile: datafile,
        author: {
          username: Authentication.getAuthenticatedAccount().username
        }
      });

      $scope.closeThisDialog();

        Snackbar.show('Success! Post created.');
      }


      /**
      * @name createPostErrorFn
      * @desc Propogate error event and show snackbar with error message
      */
      function createPostErrorFn(data, status, headers, config) {
      $rootScope.$broadcast('post.created', {
        content: vm.content,
        datafile: vm.datafile,
        author: {
          username: Authentication.getAuthenticatedAccount().username
        }
      });

      $scope.closeThisDialog();
      
        $rootScope.$broadcast('post.created.error');
        if(data.error)Snackbar.error(data.error);
        else Snackbar.error("Error inesperado!");
      }
    }
  }
})();