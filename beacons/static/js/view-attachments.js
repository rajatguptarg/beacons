(function viewAttachments(){

    var attachment = {};

    $(document).ready(function(){
        attachment.showAttchments();
    });

    attachment.showAttchments = function(){
        attachmentContainer = $("#attachmentContainer");
        attachmentJSON = JSON.parse(attachmentContainer.text());
        attachmentContainer.text(JSON.stringify(attachmentJSON, undefined, "\t"));
    }
})();
