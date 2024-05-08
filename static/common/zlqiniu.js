
'use strict';

var zlqiniu = {
	'setUp': function(args) {
		var domain = args['domain'];
		var params = {
            browse_button:args['browse_btn'],
			runtimes: 'html5,flash,html4', //upload modes, degraded in that order
			max_file_size: '500mb',  //Maximum allowed file size
			dragdrop: false, //whether to enable drag and drop uploading
			chunk_size: '4mb',  //Size of each chunk when uploading in chunks
			uptoken_url: args['uptoken_url'], //url for ajax request token
			domain: domain, //domain name for image downloads
			get_new_uptoken: false, //whether to get the token from the business server every time the file is uploaded
			auto_start: true, //If set to true, the image will be uploaded automatically as soon as it is selected.
            unique_names: true,
            multi_selection: false,
            filters: {
                mime_types :[
                    {title:'Image files',extensions: 'jpg,gif,png'},
                    {title:'Video files',extensions: 'flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4'}
                ]
            },
			log_level: 5, //log level
			init: {
				'FileUploaded': function(up,file,info) {
					if(args['success']){
						var success = args['success'];
						file.name = domain + file.target_name;
						success(up,file,info);
					}
				},
				'Error': function(up,err,errTip) {
					if(args['error']){
						var error = args['error'];
						error(up,err,errTip);
					}
				},
                'UploadProgress': function (up,file) {
                    if(args['progress']){
                        args['progress'](up,file);
                    }
                },
                'FilesAdded': function (up,files) {
                    if(args['fileadded']){
                        args['fileadded'](up,files);
                    }
                },
                'UploadComplete': function () {
                    if(args['complete']){
                        args['complete']();
                    }
                }
			}
		};

		// put the arguments from args into params
		for(var key in args){
			params[key] = args[key];
		}
		var uploader = Qiniu.uploader(params);
		return uploader;
	}
};
