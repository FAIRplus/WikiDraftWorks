var html = "text/html";
var encoding = "UTF-8";
var ClientSideResourceManager = Packages.com.google.refine.ClientSideResourceManager;
var logger = Packages.org.slf4j.LoggerFactory.getLogger("local-file-system-extension");

/*
 * Function invoked to initialize the extension.
 */
function init() {
	logger.info("Initializing local-file-system extension");
	logger.info("Local-file-system Extension Mount point " + module.getMountPoint());

	var RS = Packages.com.google.refine.RefineServlet;

	// Register importer and exporter
	var IM = Packages.com.google.refine.importing.ImportingManager;

	IM.registerController(
		module,
		"local-file-importing-controller",
		new Packages.com.refinepro.LocalFileSystemImportingController()
	);

	// Script files to inject into /index page
	ClientSideResourceManager.addPaths(
		"index/scripts",
		module,
		[
			"scripts/importing-controller.js",
			"scripts/local-data-source-ui.js"
		]
	);
	// Script files to inject into /project page
	ClientSideResourceManager.addPaths(
		"project/scripts",
		module,
		[
			"scripts/importing-controller.js",
			"scripts/local-data-source-ui.js"
		]
	);

	// Style files to inject into /project page
	ClientSideResourceManager.addPaths(
		"project/styles",
		module,
		[
			"styles/project-injection.less"
		]
	);
}

/*
 * Function invoked to handle each request in a custom way.
 */
function process(path, request, response) {

	if (path === "/" || path === "") {
		send(request, response, "index.vt", null);
	}
}

function send(request, response, template, context) {
	butterfly.sendTextFromTemplate(request, response, context, template, encoding, html);
}