// RequestHandler.js
// __author__ = Tarun

function RequestHandler(){
	this.constructor = function RequestHandler() {};
}

RequestHandler.prototype.GET = "GET";
RequestHandler.prototype.POST = "POST";
RequestHandler.prototype.PUT = "PUT";
RequestHandler.prototype.FORM_URL_ENCODED = 'application/x-www-form-urlencoded';

// RequestHandler.prototype.applyRequestHeaders = function(xhr, requestHeaders) {
//     if (typeof requestHeaders === 'undefined' || requestHeaders === null) {
//         requestHeaders = {};
//     }
//     var keys = Object.keys(requestHeaders);
//     var contentType = _.find(keys, function(key) {
//         return key.toLowerCase() == 'content-type';
//     });
//     if (contentType === undefined || contentType.toLowerCase() != 'content-type') {
//         requestHeaders['content-type'] = 'application/json';
//         keys.push('content-type');
//     }
//     keys.forEach(function(element, index, array) {
//         if (requestHeaders[element] != 'multipart/form-data')
//             xhr.setRequestHeader(element, requestHeaders[element]);
//     });
// };

RequestHandler.prototype.getContentType = function(requestHeaders) {
    if (requestHeaders !== undefined && requestHeaders !== null) {
        var requestHeadersLowered = JSON.parse(JSON.stringify(requestHeaders).toLowerCase());
        if (requestHeadersLowered['content-type'])
            return requestHeadersLowered['content-type'];
    }
    return 'application/json';
};


RequestHandler.prototype.makeRequest = function(requestUrl, httpMethod, observer, requestHeaders, dataPayload, timeoutInMillis) {
    // httpMethod = httpMethod || 'GET';
    timeoutInMillis = timeoutInMillis || 0;
    // observer = observer || $.Deferred();

    function getStatusCodeType(statusCode) {
        return parseInt(statusCode / 100) * 100;
    };

    function notifySubscribersOfError(xhr, requestUrl, dataPayload, observer) {
        var errorObject = {
            xhr: {
                status: xhr.status,
                statusText: xhr.statusText
            },
            requestUrl: requestUrl,
            dataPayload: dataPayload
        };
        observer.reject(errorObject);
    };

    var xhr = new XMLHttpRequest();
    xhr.timeout = timeoutInMillis;
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var contentType = xhr.getResponseHeader('content-type');
            var results = null;
            if (contentType.match(/text\/plain/) !== null) {
                results = xhr.responseText;
            } else if (contentType.match(/application\/json/) !== null) { // assume application/json
                results = JSON.parse(xhr.responseText);
            } else {
                results = xhr.responseText;
            }
            observer.resolve(results);

        } else if (getStatusCodeType(xhr.status) == 400) {
            notifySubscribersOfError(xhr, requestUrl, dataPayload, observer);

        } else if (getStatusCodeType(xhr.status) === 500) {
            notifySubscribersOfError(xhr, requestUrl, dataPayload, observer);

        //TODO: Check readySate for the actual value during a no-Internet situation.
        } else if (xhr.readyState == 2 && getStatusCodeType(xhr.status) === 0) { // no Internet!
            notifySubscribersOfError(xhr, requestUrl, dataPayload, observer);
        } else if (getStatusCodeType(xhr.status) == 404) {
            notifySubscribersOfError(xhr, requestUrl, dataPayload, observer);
        }

    };

    xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable) {
            var percentage = Math.round((e.loaded * 100) / e.total);
            var progressData = {};
            progressData.percentage = percentage;
            progressData.url = requestUrl;
            progressData.payload = dataPayload;
            observer.notify('upload_progress', progressData);
        }
    }, false);

    xhr.open(httpMethod, requestUrl);
    // RequestHandler.prototype.applyRequestHeaders(xhr, requestHeaders);

    if (RequestHandler.prototype.getContentType(requestHeaders).match('application/x-www-form-urlencoded') !== null) {
        var serializedDataPayload = '';
        var keys = Object.keys(dataPayload);
        keys.forEach(function(key, index) {
            serializedDataPayload += key + '=' + encodeURIComponent(dataPayload[key]) + (index === keys.length - 1 ? '' : '&');
        });
        xhr.send(serializedDataPayload);
    } else if (RequestHandler.prototype.getContentType(requestHeaders).match('application/json') !== null) {
        xhr.send(JSON.stringify(dataPayload));
    } else {
        xhr.send(dataPayload);
    }
    return observer;
};