// Copyright (c) ipylab contributors
// Distributed under the terms of the Modified BSD License.

import {
  JupyterFrontEndPlugin,
  JupyterFrontEnd,
  ILabShell
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import * as widgetExports from './widget';

import { MODULE_NAME, MODULE_VERSION } from './version';

const EXTENSION_ID = 'kishw:plugin';

/**
 * The default plugin.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: EXTENSION_ID,
  autoStart: true,
  requires: [IJupyterWidgetRegistry],
  optional: [ICommandPalette, ILabShell],
  activate: (app: JupyterFrontEnd, registry: IJupyterWidgetRegistry): void => {
    // add globals
    widgetExports.JupyterFrontEndModel.app = app;

    registry.registerWidget({
      name: MODULE_NAME,
      version: MODULE_VERSION,
      exports: widgetExports
    });
  }
};

export default extension;
