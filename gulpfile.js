var gulp = require('gulp');
var sass = require('gulp-sass');
var bs = require('browser-sync').create();
var wait = require('gulp-wait');
var exec = require('child_process').exec;

// gulp.task('browser-sync', ['sass'], function () {
//     bs.init({
//         server: {
//             baseDir: "./"
//         }
//     });
// });
gulp.task('browser-sync', ['runserver'], function() {
    bs.init({
      notify: false,
      port: 8000,
      proxy: 'localhost:8000'
    })
  });

gulp.task('runserver', function() {
    // var cmd = 'cd ..';
    var proc = exec('python manage.py runserver')
  })

gulp.task('sass', function(){
    return gulp.src('assets/scss/*.scss')
        .pipe(wait(500))
        .pipe(sass())
        .pipe(gulp.dest('static/css/'))
        .pipe(bs.reload({stream: true}));
});

gulp.task('watch', ['browser-sync', 'sass'], function() {
    gulp.watch("assets/scss/*.scss", ['sass']);
    gulp.watch("static/js/*.js").on('change', bs.reload);
    gulp.watch("**/templates/**/*.html").on('change', bs.reload);
})