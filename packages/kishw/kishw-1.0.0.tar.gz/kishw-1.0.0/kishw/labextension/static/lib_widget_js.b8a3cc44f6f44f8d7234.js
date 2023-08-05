"use strict";
(self["webpackChunkkishw"] = self["webpackChunkkishw"] || []).push([["lib_widget_js"],{

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MODULE_NAME": () => (/* binding */ MODULE_NAME),
/* harmony export */   "MODULE_VERSION": () => (/* binding */ MODULE_VERSION)
/* harmony export */ });
// Copyright (c) ipylab contributors
// Distributed under the terms of the Modified BSD License.
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
const MODULE_VERSION = data.version;
/*
 * The current package name.
 */
const MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JupyterFrontEndModel": () => (/* reexport safe */ _widgets_frontend__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEndModel),
/* harmony export */   "PanelModel": () => (/* reexport safe */ _widgets_panel__WEBPACK_IMPORTED_MODULE_1__.PanelModel),
/* harmony export */   "SplitPanelModel": () => (/* reexport safe */ _widgets_split_panel__WEBPACK_IMPORTED_MODULE_2__.SplitPanelModel),
/* harmony export */   "SplitPanelView": () => (/* reexport safe */ _widgets_split_panel__WEBPACK_IMPORTED_MODULE_2__.SplitPanelView),
/* harmony export */   "TitleModel": () => (/* reexport safe */ _widgets_title__WEBPACK_IMPORTED_MODULE_3__.TitleModel)
/* harmony export */ });
/* harmony import */ var _widgets_frontend__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./widgets/frontend */ "./lib/widgets/frontend.js");
/* harmony import */ var _widgets_panel__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widgets/panel */ "./lib/widgets/panel.js");
/* harmony import */ var _widgets_split_panel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widgets/split_panel */ "./lib/widgets/split_panel.js");
/* harmony import */ var _widgets_title__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widgets/title */ "./lib/widgets/title.js");
// Copyright (c) ipylab contributors
// Distributed under the terms of the Modified BSD License.







/***/ }),

/***/ "./lib/widgets/frontend.js":
/*!*********************************!*\
  !*** ./lib/widgets/frontend.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JupyterFrontEndModel": () => (/* binding */ JupyterFrontEndModel)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base?8add");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../version */ "./lib/version.js");
// Copyright (c) ipylab contributors
// Distributed under the terms of the Modified BSD License.


/**
 * The model for a JupyterFrontEnd.
 */
class JupyterFrontEndModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.WidgetModel {
    /**
     * The default attributes.
     */
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: JupyterFrontEndModel.model_name, _model_module: JupyterFrontEndModel.model_module, _model_module_version: JupyterFrontEndModel.model_module_version });
    }
    /**
     * Initialize a JupyterFrontEndModel instance.
     *
     * @param attributes The base attributes.
     * @param options The initialization options.
     */
    initialize(attributes, options) {
        this._app = JupyterFrontEndModel.app;
        super.initialize(attributes, options);
        this.send({ event: 'lab_ready' }, {});
        this.set('version', this._app.version);
        this.save_changes();
    }
}
JupyterFrontEndModel.serializers = Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.DOMWidgetModel.serializers);
JupyterFrontEndModel.model_name = 'JupyterFrontEndModel';
JupyterFrontEndModel.model_module = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME;
JupyterFrontEndModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;
JupyterFrontEndModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;


/***/ }),

/***/ "./lib/widgets/panel.js":
/*!******************************!*\
  !*** ./lib/widgets/panel.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PanelModel": () => (/* binding */ PanelModel)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/controls */ "webpack/sharing/consume/default/@jupyter-widgets/controls/@jupyter-widgets/controls");
/* harmony import */ var _jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../version */ "./lib/version.js");
// Copyright (c) ipylab contributors
// Distributed under the terms of the Modified BSD License.


/**
 * The model for a panel.
 */
class PanelModel extends _jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_0__.VBoxModel {
    /**
     * The default attributes.
     */
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: PanelModel.model_name, _model_module: PanelModel.model_module, _model_module_version: PanelModel.model_module_version });
    }
}
PanelModel.model_name = 'PanelModel';
PanelModel.model_module = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME;
PanelModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;


/***/ }),

/***/ "./lib/widgets/split_panel.js":
/*!************************************!*\
  !*** ./lib/widgets/split_panel.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SplitPanelModel": () => (/* binding */ SplitPanelModel),
/* harmony export */   "SplitPanelView": () => (/* binding */ SplitPanelView)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/controls */ "webpack/sharing/consume/default/@jupyter-widgets/controls/@jupyter-widgets/controls");
/* harmony import */ var _jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./panel */ "./lib/widgets/panel.js");
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../version */ "./lib/version.js");





/**
 * A Lumino widget for split panels.
 */
class JupyterLuminoSplitPanelWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.SplitPanel {
    /**
     * Construct a new JupyterLuminoSplitPanelWidget.
     *
     * @param options The instantiation options for a JupyterLuminoSplitPanelWidget.
     */
    constructor(options) {
        const view = options.view;
        // delete options.view;
        super(options);
        this.addClass('jp-JupyterLuminoSplitPanelWidget');
        this._view = view;
    }
    /**
     * Handle a lumino message.
     *
     * @param msg The message to handle.
     */
    processMessage(msg) {
        super.processMessage(msg);
        this._view.processLuminoMessage(msg);
    }
    /**
     * Dispose the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        if (this._view) {
            this._view.remove();
        }
        this._view = null;
    }
}
/**
 * The model for a split panel.
 */
class SplitPanelModel extends _panel__WEBPACK_IMPORTED_MODULE_3__.PanelModel {
    /**
     * The default attributes.
     */
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: SplitPanelModel.model_name, _model_module: SplitPanelModel.model_module, _model_module_version: SplitPanelModel.model_module_version, _view_name: SplitPanelModel.model_name, _view_module: SplitPanelModel.model_module, _view_module_version: SplitPanelModel.model_module_version });
    }
}
SplitPanelModel.model_name = 'SplitPanelModel';
SplitPanelModel.model_module = _version__WEBPACK_IMPORTED_MODULE_4__.MODULE_NAME;
SplitPanelModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_4__.MODULE_VERSION;
SplitPanelModel.view_name = 'SplitPanelView';
SplitPanelModel.view_module = _version__WEBPACK_IMPORTED_MODULE_4__.MODULE_NAME;
SplitPanelModel.view_module_name = _version__WEBPACK_IMPORTED_MODULE_4__.MODULE_VERSION;
/**
 * The view for a split panel.
 */
class SplitPanelView extends _jupyter_widgets_controls__WEBPACK_IMPORTED_MODULE_0__.VBoxView {
    /**
     * Create the widget and return the DOM element.
     *
     * @param tagName the tag name
     */
    _createElement(tagName) {
        this.luminoWidget = new JupyterLuminoSplitPanelWidget({
            view: this,
            orientation: this.model.get('orientation')
        });
        return this.luminoWidget.node;
    }
    /**
     * Set the DOM element.
     *
     * @param el The element.
     */
    _setElement(el) {
        if (this.el || el !== this.luminoWidget.node) {
            throw new Error('Cannot reset the DOM element.');
        }
        this.el = this.luminoWidget.node;
        this.$el = jquery__WEBPACK_IMPORTED_MODULE_2___default()(this.luminoWidget.node);
    }
    /**
     * Initialize a SplitPanelView instance.
     *
     * @param parameters The view parameters.
     */
    initialize(parameters) {
        super.initialize(parameters);
        const luminoWidget = this
            .luminoWidget;
        this.model.on('change:orientation', () => {
            const orientation = this.model.get('orientation');
            luminoWidget.orientation = orientation;
        });
    }
    /**
     * Render the view.
     */
    async render() {
        super.render();
        const views = await Promise.all(this.children_views.views);
        views.forEach(async (view) => {
            this.luminoWidget.addWidget(view.luminoWidget);
        });
    }
}


/***/ }),

/***/ "./lib/widgets/title.js":
/*!******************************!*\
  !*** ./lib/widgets/title.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TitleModel": () => (/* binding */ TitleModel)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base?8add");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../version */ "./lib/version.js");
// Copyright (c) ipylab contributors
// Distributed under the terms of the Modified BSD License.


/**
 * The model for a title widget.
 */
class TitleModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.WidgetModel {
    /**
     * The default attributes.
     */
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: TitleModel.model_name, _model_module: TitleModel.model_module, _model_module_version: TitleModel.model_module_version });
    }
}
TitleModel.model_name = 'TitleModel';
TitleModel.model_module = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_NAME;
TitleModel.model_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;
TitleModel.view_module_version = _version__WEBPACK_IMPORTED_MODULE_1__.MODULE_VERSION;


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"kishw","version":"0.1.0","description":"Custom widget library","keywords":["jupyter","jupyterlab","jupyterlab-extension"],"homepage":"https://github.com/github_username/kishw","bugs":{"url":"https://github.com/github_username/kishw/issues"},"license":"BSD-3-Clause","author":{"name":"Erkin","email":"erkinqara@gmail.com"},"files":["lib/**/*.{d.ts,eot,gif,html,jpg,js,js.map,json,png,svg,woff2,ttf}","style/**/*.{css,js,eot,gif,html,jpg,json,png,svg,woff2,ttf}","schema/*.json"],"main":"lib/index.js","types":"lib/index.d.ts","style":"style/index.css","repository":{"type":"git","url":"https://github.com/github_username/kishw.git"},"scripts":{"build":"jlpm build:lib && jlpm build:labextension:dev","build:prod":"jlpm clean && jlpm build:lib && jlpm build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","clean":"jlpm clean:lib","clean:lib":"rimraf lib tsconfig.tsbuildinfo","clean:lintcache":"rimraf .eslintcache .stylelintcache","clean:labextension":"rimraf kishw/labextension","clean:all":"jlpm clean:lib && jlpm clean:labextension && jlpm clean:lintcache","eslint":"jlpm eslint:check --fix","eslint:check":"eslint . --cache --ext .ts,.tsx","install:extension":"jlpm build","lint":"jlpm stylelint && jlpm prettier && jlpm eslint","lint:check":"jlpm stylelint:check && jlpm prettier:check && jlpm eslint:check","prettier":"jlpm prettier:base --write --list-different","prettier:base":"prettier \\"**/*{.ts,.tsx,.js,.jsx,.css,.json,.md}\\"","prettier:check":"jlpm prettier:base --check","stylelint":"jlpm stylelint:check --fix","stylelint:check":"stylelint --cache \\"style/**/*.css\\"","test":"jest --coverage","watch":"run-p watch:src watch:labextension","watch:src":"tsc -w","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1 || ^2 || ^3 || ^4 || ^5 || ^6","@jupyter-widgets/controls":"^3 || ^4 || ^5","@jupyterlab/application":"^3.5.1","@jupyterlab/apputils":"^3.5.1","@jupyterlab/observables":"^4.5.1","@lumino/algorithm":"^1.9.2","@lumino/commands":"^1.20.1","@lumino/disposable":"^1.10.2","@lumino/messaging":"^1.10.2","@lumino/widgets":"^1.34.0","@jupyterlab/settingregistry":"^3.5.1","@jupyterlab/coreutils":"^5.5.1","@jupyterlab/services":"^6.5.1","react":"18.2.0","react-dom":"18.2.0"},"devDependencies":{"@babel/core":"^7.0.0","@babel/preset-env":"^7.0.0","@jupyterlab/builder":"^3.5.1","@jupyterlab/testutils":"^3.5.1","@types/jest":"^26.0.0","jest":"^26.0.0","stylelint":"^14.3.0","stylelint-config-prettier":"^9.0.4","stylelint-config-recommended":"^6.0.0","stylelint-config-standard":"~24.0.0","stylelint-prettier":"^2.0.0","ts-jest":"^26.0.0","@types/expect.js":"^0.3.29","@types/node":"^18.7.8","@typescript-eslint/eslint-plugin":"^5.33.1","@typescript-eslint/parser":"^5.33.1","eslint":"^8.22.0","eslint-config-prettier":"^8.5.0","eslint-plugin-jsdoc":"^39.3.6","eslint-plugin-prettier":"^4.2.1","eslint-plugin-react":"^7.30.1","expect.js":"^0.3.1","fs-extra":"^10.1.0","husky":"^8.0.1","lint-staged":"^13.0.3","mkdirp":"^1.0.4","npm-run-all":"^4.1.5","prettier":"^2.7.1","rimraf":"^3.0.2","typescript":"~4.7.4"},"sideEffects":["style/*.css","style/index.js"],"styleModule":"style/index.js","publishConfig":{"access":"public"},"jupyterlab":{"extension":"lib/plugin","outputDir":"kishw/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.b8a3cc44f6f44f8d7234.js.map