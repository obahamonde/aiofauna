<template>
  <div class="navbar-fixed">
    <nav class="nav-extended white">
      <div class="nav-wrapper white">
        <ul>
          <li><a href="#!" class="title grey-text text-darken-1">Google Drive</a></li>
        </ul>
        <div class="search-wrapper">
          <i class="material-icons">search</i>
          <input type="search" name="Search" placeholder="Search Drive" />
        </div>
        <ul class="right">
          <li><a href="#!"><i class="material-icons grey-text text-darken-1">apps</i></a></li>
          <li><a href="#!"><i class="material-icons grey-text text-darken-1">notifications</i></a></li>
          <li><a href="#!"><img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/40532/profile/profile-80.jpg"
                class="circle"></a></li>
        </ul>
      </div>
      <div class="nav-wrapper nav-2">
        <ul>
          <li><a class="waves-effect waves-light btn btn-flat white-text">New</a></li>
        </ul>
        <ul class="right">
          <li><a href="#!"><i class="material-icons grey-text text-darken-1">view_list</i></a></li>
          <li><a href="#!"><i class="material-icons grey-text text-darken-1">info</i></a></li>
          <li><a href="#!"><i class="material-icons grey-text text-darken-1">settings</i></a></li>
        </ul>
      </div>
    </nav>
  </div>
</template>
<style global lang="sass">
// It is not THE google drive design, it is similar & inspired by drive.google.com

// Colors
$main-white: #fff

$main-grey: #f0f0f0
$menu-light-grey: #e7e7e7
$menu-grey: #e1e1e1
$input-grey: #7e7e7e
$menu-dark-grey: #454545

$icloud-blue: #10b0ff
$main-blue: #0191ff
$hover-blue: #0174d7

$main-yellow: #e7a200

// Transitions
$main-transition: all 0.5s ease
$input-transition: background 0.5s ease
$btn-transition: color 0.5s ease, border-color 0.5s ease

// Shadows
$main-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)
$card-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)


*
  font-family: 'Roboto', sans-serif
  &::-webkit-scrollbar-track
    background: transparent
  &::-webkit-scrollbar
    width: 8px
  &::-webkit-scrollbar-thumb
    background: transparent
  &:hover
    &::-webkit-scrollbar-thumb
      border-radius: 4px
      outline: 1px solid slategray
      background-color: darkgray
html
  height: 100%
body
  height: 100%
  background: $main-grey
  overflow-y: hidden
header
  width: 100%
  background: $main-white
  padding: 15px
  box-shadow: $main-shadow
  position: fixed
  top: 0
  z-index: 10
  .row
    .col-xs-1, .col-md-1
      padding-top: 7px
.search-form
  position: relative
  width: 100%
  max-width: 700px
  margin: 0 auto
  .search-icon
    position: absolute
    top: 15px
    left: 15px
    i
      font-size: 22px
      color: $input-grey
  .search-input
    background: $main-grey
    width: 100%
    max-width: 700px
    padding: 10px 10px 10px 50px
    font-size: 20px
    border-radius: 3px
    border: 1px solid transparent
    transition: $input-transition
    &:focus
      outline: none
      background: $main-white
      box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)
      border-color: $main-grey
    &::placeholder
      font-size: 18px
      font-weight: 100
      color: $input-grey
.se-btn
  display: block
  width: 100%
  text-align: center
  padding: 10px 15px
  cursor: pointer
  border-radius: 3px
  transition: $input-transition
.blue-btn
  @extend .se-btn
  background: $main-blue
  color: $main-white
  &:hover
    text-decoration: none
    background: $hover-blue
    color: $main-white
  i
    margin-right: 5px
.white-btn
  @extend .se-btn
  border: 2px solid $menu-grey
  color: $input-grey
  background: $main-white
  transition: $btn-transition
  &:hover
    border: 2px solid $main-blue
    color: $main-blue
    text-decoration: none
  i
    margin-right: 5px
.logo
  font-size: 30px
  font-weight: bold
  color: #000
  &:hover
    color: #000
    text-decoration: none
    cursor: pointer
.main
  padding-top: 80px
  position: relative
  display: block
  overflow-y: hidden
  height: 100%
  .row
    height: 100%
.main-content, .sidebar, .menu
  height: 100%
  padding-top: 25px
.menu
  padding-left: 0
  nav
    ul
      padding: 0
      li
        list-style: none
        a
          width: 100%
          padding: 12px 20px
          display: block
          color: $menu-dark-grey
          font-size: 14px
          font-weight: bold
          &:hover
            background: $menu-light-grey
            border-top-left-radius: 3px
            border-top-right-radius: 3px
          &:hover
            text-decoration: none
            color: $menu-dark-grey
          i
            margin-right: 15px
        .active
          background: $menu-grey
          border-top-left-radius: 3px
          border-top-right-radius: 3px
          i
            color: $main-blue
      .trenner
        border-top: 1px solid $menu-grey
        padding-top: 10px
        margin-top: 10px
.sidebar
  background: $main-white
  position: relative
  z-index: 5
  box-shadow: $main-shadow
  padding: 0
  h2
    color: $input-grey
    padding-left: 25px
    font-size: 20px
  p
    padding: 0 25px
    margin-bottom: 15px
    &:last-of-type
      margin-bottom: 35px
.info
  border-bottom: 1px solid $main-grey
  margin: 15px 0 0 0
  text-align: center
  h3
    font-size: 14px
    margin: 0
    padding-bottom: 10px
    text-align: center
    text-transform: uppercase
  .row
    height: auto
    min-height: 0
.info-link
  border-bottom: 3px solid transparent
  display: inline-block
  color: $menu-dark-grey
  padding: 0 20px
  &:hover
    border-color: $menu-dark-grey
    text-decoration: none
    color: $menu-dark-grey
  &:first-of-type
    margin-right: 25px
.info-active-link
  border-bottom: 3px solid $main-blue!important
  color: $main-blue!important
  &:hover
    cursor: default
    color: $main-blue!important
.main-content
  padding-right: 35px
  overflow-y: auto
.card
  background: $main-white
  border-radius: 3px
  width: 100%
  min-height: 150px
  box-shadow: $card-shadow
  cursor: pointer
  display: block
  transition: all 0.3s cubic-bezier(.25,.8,.25,1)
  &:hover
    text-decoration: none
    box-shadow: $main-shadow
  .card-header
    height: 75px
    color: $main-white
    text-align: center
    font-size: 30px
    padding-top: 15px
    border-top-left-radius: 3px
    border-top-right-radius: 3px
  .card-content
    padding: 15px
    color: $input-grey
    h2
      margin: 0
      font-size: 16px
    p
      margin: 10px 0 0 0
      font-size: 12px
.google
  @extend .card-header
  background: $main-yellow
.icloud
  @extend .card-header
  background: $icloud-blue
.onedrive
  @extend .card-header
  background: $hover-blue
.dropbox
  @extend .card-header
  background: $main-blue
.server-name
  font-size: 22px
  color: $menu-dark-grey
  margin-top: 30px
.file-legend
  color: $input-grey
  margin-top: 10px
  padding-left: 15px
.files
  margin-top: 5px
  background: $main-white
  width: 100%
  min-height: 250px
  border: 1px solid $menu-grey
.file-row
  border-bottom: 1px solid $menu-grey
  width: 100%
  height: 50px
  &:last-of-type
    border-bottom: 0
  .row
    padding-top: 15px
    padding-left: 15px
.file-icon
  margin-right: 10px

// Bootstrap Korrekturen
.col-md-2
  transition: $main-transition
.container-fluid
  overflow-y: hidden

@media screen and (max-width: 991px)
  .sidebar
    display: none

</style>
