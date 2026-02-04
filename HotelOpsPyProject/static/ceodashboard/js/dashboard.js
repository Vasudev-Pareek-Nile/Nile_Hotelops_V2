

let selectedTimeRange = null;

function setDateInputValue() {
    try {
        const dateInput = document.getElementById("date_Hotelrevenue");
        if (!dateInput) {
            console.warn("Date input element not found. ID: 'date_Hotelrevenue'");
            return; 
        }
        const today = new Date();
        today.setDate(today.getDate() - 1); 
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${year}-${month}-${day}`;
    } catch (error) {
        console.error("An error occurred while setting the date input value:", error.message);
        
    }
}



// const dateInput = document.getElementById("date_Hotelrevenue");
// const today = new Date();
// today.setDate(today.getDate() - 1); // Set to yesterday


// const year = today.getFullYear();
// const month = String(today.getMonth() + 1).padStart(2, '0');
// const day = String(today.getDate()).padStart(2, '0');


// dateInput.value = `${year}-${month}-${day}`;


function showLoader(chartType) {
    document.getElementById(`loader-${chartType}`).style.display = 'flex';
}


function hideLoader(chartType) {
    document.getElementById(`loader-${chartType}`).style.display = 'none';
}

async function viewLeave(t, e, o, n, l, d, s) {
   
    $(".LeaveModal").modal("show"),
        $(".LeaveModal #sp_LeaveType").text(n),
        $(".LeaveModal #sp_From").text(l),
        $(".LeaveModal #sp_To").text(d),
        $(".LeaveModal #sp_Reason").text(s),
        $(".LeaveModal #id").val(e),
        $(".LeaveModal #oid").val(o);
        $(".LeaveModal #UserID").val(UserID); 

}

viewIA = function (t, e, o) {
    let a = '';
    $(".IAModal .modal-footer").empty(),
        $(".IAModal").modal("show"),
        $(".IAModal iframe").attr("src", GRedURL+"/InterviewAssessment/Home/View/" + e),
        $(".IAModal iframe").on("load", function () {
            var t = document.getElementById("IAiframe"),
                e = t.contentDocument || t.contentWindow.document,
                o = e.getElementsByClassName("navbar-default");
            o.length > 0 && (o[0].style.display = "none");
            var n = e.getElementsByClassName("navbar");
            n.length > 0 && (n[0].style.display = "none");
        }),
        (a += '<span type="button" class="btn btn-secondary" data-dismiss="modal">Close</span>'),
        $(".IAModal .modal-footer").append(a);
};

ViewExitForm = function (t, e,o) {
    $(".ExitFormModal .modal-footer").empty(), $(".ExitFormModal").modal("show"), $(".ExitFormModal iframe").attr("src", GRedURL+"/ExitInterview/home/ViewDetails/" + e + "?i=" + o);
};



SaveApproveLeaveapplication = function (t) {
    $(".LeaveModal [name='oid']").val(), $(".LeaveModal [name='id']").val(), $(".LeaveModal [name='Type']").val();
};

SaveApproveCapex = function (t) {
        var e = $(".capexmodalAppRej [name='OID']").val(),
            o = $(".capexmodalAppRej [name='ID']").val(),
            n = $(".capexmodalAppRej [name='Status']").val(),
            l = $(".capexmodalAppRej [name='Remarks']").val(),
            d = $(".capexmodalAppRej [name='Qty']").val(),
            s = $(".capexmodalAppRej [name='Type']").val();
        $.ajax({
            async: !1,
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: GRedURL+"/api/CapexAPI/Approved?ID=" + o + "&Status=" + n + "&Remarks=" + l + "&Qty=" + d + "&Type=" + s + "&OID=" + e,
            dataType: "json",
            success: function (t) {
                if (void 0 != t && null != t) {
                    switch (($("tr[data-i='" + o + "'] .td_" + s + "_s").empty(), n)) {
                        case "Approved":
                            $("tr[data-i='" + o + "'] .td_" + s + "_s").append(' <label class="btn btn-sm btn-success">Approved</label>');
                            break;
                        case "Rejected":
                            $("tr[data-i='" + o + "'] .td_" + s + "_s").append(' <label class="btn btn-sm btn-danger">Rejected</label>');
                            break;
                        case "Returned":
                            $("tr[data-i='" + o + "'] .td_" + s + "_s").append(' <label class="btn btn-sm btn-danger">Returned</label>');
                            break;
                        case "Hold":
                            $("tr[data-i='" + o + "'] .td_" + s + "_s").append(' <label class="btn btn-sm btn-warning">Hold</label>');
                    }
                    $("tr[data-i='" + o + "'] .td_" + s + "_s").append("<p>Qty:" + d + "</p>"),
                        $("tr[data-i='" + o + "'] .td_" + s + "_s").append("<p>Remarks:" + l + "</p>"),
                        $("tr[data-i='" + o + "'] .button-group [onclick*='ActiveShowRej']").hide(),
                        $(".capexmodalAppRej [name='Status']").val(""),
                        $(".capexmodalAppRej [name='Qty']").val(""),
                        $(".capexmodalAppRej").modal("hide");
                        RDCapex() 
                }
            },
        });
    };
CapexActiveShowRej = function (t, e, o, n, l) {
    switch (
    ((n = void 0 == n ? 0 : n),
        $(".capexmodalAppRej [name='Qty']").addClass("hide"),
        $(".capexmodalAppRej [name='ID']").val(e),
        $(".capexmodalAppRej [name='OID']").val(l),
        $(".capexmodalAppRej [name='Status']").val(""),
        $(".capexmodalAppRej [name='Qty']").val(""),
        $(".capexmodalAppRej [name='Remarks']").val(""),
        $(".capexmodalAppRej [name='Type']").val(o),
        $(".capexmodalAppRej .btnA").text("Approved"),
        $(".capexmodalAppRej .btnA").removeClass("btn-danger").removeClass("btn-primary").addClass("btn-primary"),
        $(".capexmodalAppRej .modal-header").removeClass("label-danger"),
        t)
    ) {
        case "a":
            $(".capexmodalAppRej .modal-title").text("Approve"),
                $(".capexmodalAppRej [name='Status']").val("Approved"),
                $(".capexmodalAppRej [name='Qty']").removeClass("hide"),
                $(".capexmodalAppRej [name='Qty']").val(n),
                $(".capexmodalAppRej [name='Qty']").attr("required", "required");
            break;
        case "h":
            $(".capexmodalAppRej .modal-title").text("Hold"),
                $(".capexmodalAppRej [name='Status']").val("Hold"),
                $(".capexmodalAppRej [name='Qty']").val(n),
                $(".capexmodalAppRej .btnA").text("Hold"),
                $(".capexmodalAppRej .btnA").addClass("btn-warning");
            break;
        case "r":
            $(".capexmodalAppRej .modal-title").text("Reject"),
                $(".capexmodalAppRej .modal-header").addClass("label-danger"),
                $(".capexmodalAppRej .btnA").text("Rejected"),
                $(".capexmodalAppRej [name='Qty']").val(n),
                $(".capexmodalAppRej .btnA").addClass("btn-danger"),
                $(".capexmodalAppRej [name='Status']").val("Rejected");
            break;
        case "rt":
            $(".capexmodalAppRej .modal-title").text("Return"),
                $(".capexmodalAppRej .modal-header").addClass("label-danger"),
                $(".capexmodalAppRej .btnA").text("Return"),
                $(".capexmodalAppRej [name='Qty']").val(n),
                $(".capexmodalAppRej .btnA").addClass("btn-danger"),
                $(".capexmodalAppRej [name='Status']").val("Returned");
    }
    $(".capexmodalAppRej").modal("show");
 $(".capexModal").modal("hide");
};

viewPADP = function (t, e, o, n, l) {
    $(".padpModal .modal-footer").empty(),
        $(".padpModal").modal("show"),
        "Manager" == l ? $(".padpModal iframe").attr("src", GRedURL+"/KRA/PADP/ViewMGRPADP?U=" + o + "&ID=" + e + "&O=" + n) : $(".padpModal iframe").attr("src", GRedURL+"/KRA/PADP/ViewAPADP?U=" + o + "&ID=" + e + "&O=" + n);
    var d = '<span class="btn btn-primary   " onclick="PADPActiveShowRej(\'a\',' + e + ",'" + l + "','',this," + n + ')" title="Approve"><i class="glyphicon glyphicon-check"></i> Approve</span>';
    (d += '<span class="btn btn-primary   " onclick="PADPActiveShowRej(\'r\',' + e + ",'" + l + "','',this," + n + ')" title="Return"><i class="glyphicon glyphicon-remove"></i> Return</span>'),
        (d += '<span type="button" class="btn btn-secondary" data-dismiss="modal">Close</span>'),
        $(".padpModal .modal-footer").append(d);
};

PADPActiveShowRej = function (t, e, o, n, l, d, s) {
    if (($(".PADPmodalAppRej [name='Remarks']").val(""), $(".PADPmodalAppRej [name='RUOI']").val(d), void 0 != n && "" != n)) "sal" == n ? ActiveShowCRTRej(t, e, o, n, l, d, s) : ActiveShowCRTPRej(t, e, o, n, l, d, s);
    else {
        switch (
        ($(".PADPmodalAppRej [name='ID']").val(e),
            $(".PADPmodalAppRej [name='OID']").val(d),
            $(".PADPmodalAppRej [name='Status']").val(""),
            $(".PADPmodalAppRej [name='RT']").val(o),
            $(".PADPmodalAppRej [name='ut']").val(s),
            $(".PADPmodalAppRej .btnA").text("Approved"),
            $(".PADPmodalAppRej .btnA").removeClass("btn-danger").removeClass("btn-primary").addClass("btn-primary"),
            $(".PADPmodalAppRej .modal-header").removeClass("label-danger"),
            t)
        ) {
            case "a":
                $(".PADPmodalAppRej .modal-title").text("Approve"), $(".PADPmodalAppRej [name='Status']").val("Approved");
                break;
            case "r":
                $(".PADPmodalAppRej .modal-title").text("Returned"),
                    $(".PADPmodalAppRej .modal-header").addClass("label-danger"),
                    $(".PADPmodalAppRej .btnA").text("Submit"),
                    $(".PADPmodalAppRej .btnA").addClass("btn-danger"),
                    $(".PADPmodalAppRej [name='Status']").val("Returned");
        }
        $(".PADPmodalAppRej").modal("show");
    }
};







document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    fetch('api/all_leaves_ceo/')
        .then(response => response.json())
        .then(data => {
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                buttonText: {
                    today: 'Today',
                    dayGridMonth: 'Month',
                    timeGridWeek: 'Week',
                    timeGridDay: 'Day'
                },
                events: data.Table.map(event => ({
                    ...event,
                    classNames: ['my-custom-event'] 
                })),
                eventDidMount: function (info) {
                    var tooltip = document.createElement('div');
                    tooltip.className = 'tooltip1'; 
                    tooltip.innerHTML = info.event.title; 

                    
                    document.body.appendChild(tooltip);

                    
                    tooltip.style.position = 'absolute';
                    tooltip.style.display = 'none'; 

                    
                    info.el.addEventListener('mouseenter', function (event) {
                        tooltip.style.display = 'block'; 
                        tooltip.style.top = (event.clientY + 10) + 'px'; 
                        tooltip.style.left = (event.clientX + 10) + 'px'; 
                    });

                    
                    info.el.addEventListener('mouseleave', function () {
                        tooltip.style.display = 'none'; 
                    });
                },
            });

            calendar.render();
        })
        .catch(error => console.error('Error fetching hotel chart data:', error));
});

async function ShowGlitchDetails(chartType){
    try {
        const RT = selectedTimeRange
        document.getElementById('GlitchDetailsModal').style.display = 'block';
        showLoader(chartType);

        const response = await fetch(`api/GlitchDetails/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }


        const data = await response.json();
        glitchDataCache=data.GlitchData
        const totalCount = glitchDataCache.length;
        const openCount = glitchDataCache.filter(item => item.Status === 'Open').length;
        const closedCount = glitchDataCache.filter(item => item.Status === 'Close').length;
        document.querySelector('.btn_total_glitch').innerText = totalCount;
        document.querySelector('.btn_open_glitch').innerText = openCount;
        document.querySelector('.btn_close_glitch').innerText = closedCount;
        const tableBody = document.getElementById('tblGlitchDetailsBody');
        tableBody.innerHTML = '';

        data.GlitchData.forEach((item ,index)=> {
            const row = `
                <tr data-status="${item.Status}">
                    <td>${index + 1 }</td>
                    <td>${item.Hotel}</td>
                    <td>${item.GuestName}</td>
                    <td>${item.CompanyName}</td>
                    <td>${item.Complaint}</td>
                    <td>${item.ServiceRecovery}</td>
                    <td>${item.ProcessLapse}</td>
                    <td>${item.ProcessLapseCategory}</td>
                    <td>${item.GMComment}</td>
                    <td>${item.Status}</td>
                    <td>${item.CreatedOn}</td>
                    <td><a target="_blank" style="color:blue" class="fa fa-eye" href="${GRedURL}/Glitch/Home/ExportGlitch?I=${item.ID}&amp;O=${item.OID}"></a> <a target="_blank" style="color:Red" class="fa fa-file-pdf-o" href="${GRedURL}/Glitch/Home/ExportGlitch?I=${item.ID}&amp;O=${item.OID}&amp;IsD=True"></a></td>  
                </tr>
            `;
            tableBody.innerHTML += row;
            
        });

        filterTableByStatus(status);
       
        hideLoader(chartType);
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching glitch Details data:', error);
    }

}
function filterTableByStatus(status) {
    const rows = document.querySelectorAll('#tblGlitchDetailsBody tr');
    rows.forEach(row => {
    const rowStatus = row.getAttribute('data-status');
    if (status === '' || rowStatus === status) {
        row.style.display = ''; 
    } else {
        row.style.display = 'none'; 
    }
    });
}
function ToggleGlitch(status) {
     filterTableByStatus(status); 
}

async function ShowCompRoomDetails(chartType) {
    try {
        const RT = selectedTimeRange
        document.getElementById('CompRoomDetailsModal').style.display = 'block';
        showLoader(chartType);
        const response = await fetch(`api/CompRoomDetails/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        const tableBody = document.getElementById('compRoomDetailsBody');
        tableBody.innerHTML = '';

        data.CompRoomData.forEach((item, index) => {
            const row = `
                <tr>
                    <td>${index + 1}</td>
                    <td>${item.Hotel}</td>
                    <td>${item.GuestName}</td>
                    <td>${item.CompanyName}</td>
                    <td>${item.NoRoom}</td>
                    <td>${item.ArrivalDate}</td>
                    <td>${item.DepartureDate}</td>
                    <td style="text-align:center"><span class="${item.CompRoomStatus == 2 ? 'AcceptCircle' : 'RejectCircle'}"></span></td>
                    <td><a target="_blank" style="color:Red" class="fa fa-file-pdf-o" href="${GRedURL}/CompRoom/Home/ViewPDF?VID=${item.ID}"></a></td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });


       
        hideLoader(chartType);



    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching CompRoomDetails data:', error);
    }
}


async function ShowIncidentDetails(chartType){
    try {
        const RT = selectedTimeRange
        document.getElementById('IncidentDetailsModal').style.display = 'block';
        showLoader(chartType);

        const response = await fetch(`api/IncidentDetails/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }


        const data = await response.json();
        const tableBody = document.getElementById('IncidentDetailsBody');
        tableBody.innerHTML = '';
        

        data.IncidentData.forEach((item ,index)=> {
            const row = `
            <tr>
                <td>${index + 1}</td>
                <td>${item.Hotel}</td>
                <td>${item.Location}</td>
                <td>${item.IncidentDate}</td>
                <td>${item.Description}</td>
                <td>${item.AccidentCause}</td>
                <td>${item.Anycasualty}</td>
                <td>${item.Damagedcaused}</td>
                <td>${item.Investigation}</td>
                <td><a target="_blank" style="color:blue" class="fa fa-eye" href="${GRedURL}/IncidentReport/Home/ViewDetails?VID=${item.ID}"></a> <a target="_blank" style="color:Red" class="fa fa-file-pdf-o" href="${GRedURL}/IncidentReport/Home/ViewDetails?VID=${item.ID}&amp;IsD=True"></a></td>
            </tr>
        `;
        tableBody.innerHTML += row;
        });


        
        hideLoader(chartType);
    } 
    catch (error) {
        hideLoader(chartType);
        console.error('Error fetching IncidentDetails data:', error);
    }
}

async function ShowTotalEquipment() {
    try {
        const RT = selectedTimeRange;
        $('#EnqEQDetailsModal').modal('show');
        showLoader('showTotalEquip');

        const detailResponse = await fetch(`api/CEOEngineeringTotalEquipmentDetailsData/?RT=${RT}`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

        const detailData = await detailResponse.json();
        const toprequestbody = document.getElementById('EnqEQDetailsModalBody');


        toprequestbody.innerHTML = ''; 

        detailData.Table.forEach((detail, index) => {
        
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${index + 1}</td>
        <td >${detail.Hotel} </td>
        <td >${detail.Descriptions}</td>
        <td >${detail.Area}</td>
        <td >${detail.Department} </td>
        <td >${detail.WarrantyEndDate}</td>
        <td >${detail.Status}</td>
        <td >${detail.AMCEndDate}</td>
        <td >${detail.AStatus}</td>
        `;
        toprequestbody.appendChild(row);
        }); 
        hideLoader('showTotalEquip')            
        
    } catch (error) {
    hideLoader('showTotalEquip')      
    console.error('Error fetching EnqEQDetailsModal data:', error);
    document.getElementById('EnqEQDetailsModalBody').innerText = 'Error fetching details.';
    }
}

async function ShowTotalUWEquipment() {
try {
    const RT = selectedTimeRange;
    $('#EnqEQDetailsModal').modal('show');
    showLoader('showTotalEquip');
    const detailResponse = await fetch(`api/CEOEngineeringTotalUWEquipmentDetailsData/?RT=${RT}`);
    if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
    const detailData = await detailResponse.json();
    const toprequestbody = document.getElementById('EnqEQDetailsModalBody');
    toprequestbody.innerHTML = ''; 
    detailData.Table.forEach(( detail, index) => {
    
    const row = document.createElement('tr');
    row.innerHTML = `
    <td>${index + 1}</td>
    <td >${detail.Hotel} </td>
    <td >${detail.Descriptions}</td>
    <td >${detail.Area}</td>
    <td >${detail.Department} </td>
    <td >${detail.WarrantyEndDate}</td>
    <td >${detail.Status}</td>
    <td >${detail.AMCEndDate}</td>
    <td >${detail.AStatus}</td>
    `;
    toprequestbody.appendChild(row);
    });
    hideLoader('showTotalEquip')      
                    
    
    
} 
catch (error) {
        hideLoader('showTotalEquip')      
        console.error('Error fetching EnqEQDetailsModal data:', error);
        document.getElementById('EnqEQDetailsModalBody').innerText = 'Error fetching details.';
 }
}

async function ShowTotalUAEquipment() {
    try {
        const RT = selectedTimeRange;
        $('#EnqEQDetailsModal').modal('show');
        showLoader('showTotalEquip');
        const detailResponse = await fetch(`api/CEOEngineeringTotalUAEquipmentDetailsData/?RT=${RT}`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
        const detailData = await detailResponse.json();
        const toprequestbody = document.getElementById('EnqEQDetailsModalBody');
        toprequestbody.innerHTML = ''; 
        detailData.Table.forEach((detail ,index)=> {
        
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${index + 1}</td>
        <td >${detail.Hotel} </td>
        <td >${detail.Descriptions}</td>
        <td >${detail.Area}</td>
        <td >${detail.Department} </td>
        <td >${detail.WarrantyEndDate}</td>
        <td >${detail.Status}</td>
        <td >${detail.AMCEndDate}</td>
        <td >${detail.AStatus}</td>
        `;
        toprequestbody.appendChild(row);
        });
        hideLoader('showTotalEquip')      
  
       
    
    } 
    catch (error) {
        hideLoader('showTotalEquip')      
        console.error('Error fetching EnqEQDetailsModal data:', error);
        document.getElementById('EnqEQDetailsModalBody').innerText = 'Error fetching details.';
    }
}

async function ShowTotalBreakdown(){
    try {
        $('#EnqEQBreakdownDetailsModal').modal('show');
        showLoader('showTotalbreakdown');
        const RT = selectedTimeRange
        const detailResponse = await fetch(`api/CEOEngineeringTotalBreakdownDetailsData/?RT=${RT}`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
        const detailData = await detailResponse.json();
        const toprequestbody = document.getElementById('EnqEQBreakdownDetailsModalbody');
        toprequestbody.innerHTML = ''; 
        detailData.Table.forEach((detail ,index)=> {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${index + 1}</td>
        <td >${detail.Hotel} </td>
        <td >${detail.Descriptions}</td>
        <td >${detail.Area}</td>
        <td >${detail.Department} </td>
        <td >${detail.WarrantyEndDate}</td>
        <td >${detail.Status}</td>
        <td >${detail.AMCEndDate}</td>
        <td >${detail.AStatus}</td>
        <td >${detail.BreakdownDate}</td>
        <td >${detail.MStatus}</td>
        <td >${detail.BreakdownReason}</td>
        <td >${detail.Amount}</td>
        `;
        toprequestbody.appendChild(row);
        });
        hideLoader('showTotalbreakdown')      

                    
        
                
    } 
    catch (error) {
        hideLoader('showTotalbreakdown')      
        console.error('Error fetching EnqEQBreakdownDetailsModal data:', error);
        document.getElementById('EnqEQBreakdownDetailsModalbody').innerText = 'Error fetching details.';
    }
}


async function ShowTotalMaintenance(){
    try {
        const RT = selectedTimeRange;
        $('#EnqEQMaintanceDetailsModal').modal('show');   
        showLoader('showTotalmaintance');
        const detailResponse = await fetch(`api/CEOEngineeringTotalMaintenanceDetailsData/?RT=${RT}`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
        const detailData = await detailResponse.json();
        const toprequestbody = document.getElementById('EnqEQMaintanceDetailsModalbody');
        toprequestbody.innerHTML = ''; 
        detailData.Table.forEach((detail ,index)=> {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${index + 1}</td>
        <td >${detail.Hotel} </td>
        <td >${detail.Descriptions}</td>
        <td >${detail.Area}</td>
        <td >${detail.Department} </td>
        <td >${detail.WarrantyEndDate}</td>
        <td >${detail.Status}</td>
        <td >${detail.AMCEndDate}</td>
        <td >${detail.AStatus}</td>
        <td >${detail.MaintenanceDate}</td>
        <td >${detail.MStatus}</td>
                `;
            toprequestbody.appendChild(row);
        });
        hideLoader('showTotalmaintance')      

                            
           
    } 
    catch (error) {
            hideLoader('showTotalmaintance') 
            console.error('Error fetching EnqEQMaintanceDetailsModal data:', error);
            document.getElementById('EnqEQMaintanceDetailsModalbody').innerText = 'Error fetching details.';
    }
}


async function ShowTotalPendingMaintenance(){
    try {
        const RT = selectedTimeRange
        $('#EnqEQMaintanceDetailsModal').modal('show');
        showLoader('showTotalmaintance');
        const detailResponse = await fetch(`api/CEOEngineeringTotalPendingMaintenanceDetailsData/?RT=${RT}`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
        const detailData = await detailResponse.json();
        const toprequestbody = document.getElementById('EnqEQMaintanceDetailsModalbody');
        toprequestbody.innerHTML = ''; 
        detailData.Table.forEach((detail ,index)=> {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${index + 1}</td>
        <td >${detail.Hotel} </td>
        <td >${detail.Descriptions}</td>
        <td >${detail.Area}</td>
        <td >${detail.Department} </td>
        <td >${detail.WarrantyEndDate}</td>
        <td >${detail.Status}</td>
        <td >${detail.AMCEndDate}</td>
        <td >${detail.AStatus}</td>
        <td >${detail.MaintenanceDate}</td>
        <td >${detail.MStatus}</td>
        `;
        toprequestbody.appendChild(row);
        });

        hideLoader('showTotalmaintance') 

        
            
        } 
    catch (error) {
        hideLoader('showTotalmaintance') 
            console.error('Error fetching EnqEQMaintanceDetailsModal data:', error);
            document.getElementById('EnqEQMaintanceDetailsModalbody').innerText = 'Error fetching details.';
    }
}

function closeModalComp() {
    document.getElementById('CompRoomDetailsModal').style.display = 'none';
}
function closeGlitchModal() {
    document.getElementById('GlitchDetailsModal').style.display = 'none';
}
function closeIncidentModal() {
    document.getElementById('IncidentDetailsModal').style.display = 'none';
}


document.addEventListener("DOMContentLoaded", function () {
    const firstButton = document.querySelector('.btn-group button:first-child');
    const pageId = document.body.id;
    switch (pageId) {
        case 'CeoDashboard':
            setDateInputValue();
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData();
            CEORevenueTotalData(firstButton,'CEOData', 1);
            forecastDatachart(firstButton, 'occ',1);
            forecastAdrDatachart(firstButton,'adr', 1);
            payMasterDatachart(firstButton,'paymaster', 1);
            SalesContractChartData(firstButton,'sc', 1);
            DSRChart(firstButton,'dsr',1);
            out_of_orderChart(firstButton,'outoforder', 1);
            total_SRMSRequestChart(firstButton,'srms', 1);
            RDGuestMetChart(firstButton,'GMguest', 1);
            ArCollectionDatachart(firstButton,'arc', 1);
            PpmRoomsDatachart(firstButton,'PPM', 1);
            TopSRMSrequestChart(firstButton,'topSRMS', 1);
            total_SRMSRequestCompletionChart(firstButton,'totalSRMS', 1);
            maintanceBreakdown(firstButton,'maintance', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            warningLettersDatachart(firstButton,'warnletter', 1);
            cateringSaleDatachart(firstButton,'catering', 1);
            dailyBreakageDataChart(firstButton,'breakreport', 1);
            restaurantFeedbackDataChart(firstButton,'feedback', 1);
            ConsumptionDataChart(firstButton,'csd', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            CEODashboardMasterData();
            RDGatepass();
            MOMList();
            FollowUps();
            MainingGuideChart('mainingGuide');
            organizationList();
    
            break;
        case 'RoomDivisionDashboard':
            HotelRevenueDataChart1(firstButton,'htlissue', 1);
            payMasterDatachart(firstButton,'paymaster', 1);
            out_of_orderChart(firstButton,'outoforder', 1);
            total_SRMSRequestChart(firstButton,'srms', 1);
            RDGuestMetChart(firstButton,'GMguest', 1);
            PpmRoomsDatachart(firstButton,'PPM', 1);
            TopSRMSrequestChart(firstButton,'topSRMS', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            total_SRMSRequestCompletionChart(firstButton,'totalSRMS', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            MainingGuideChart('mainingGuide');
            RDEmpResignation();
            FollowUps();
            break;
        

        case 'EngineeringDashboard':
            HotelRevenueDataChart1(firstButton,'htlissue', 1);
            out_of_orderChart(firstButton,'outoforder', 1);
            PpmRoomsDatachart(firstButton,'PPM', 1);
            maintanceBreakdown(firstButton,'maintance', 1);
            total_SRMSRequestChart(firstButton,'srms', 1);
            TopSRMSrequestChart(firstButton,'topSRMS', 1);
            total_SRMSRequestCompletionChart(firstButton,'totalSRMS', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            organizationList();
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            MainingGuideChart('mainingGuide');
            RDEmpResignation();
            RDGatepass();
            FollowUps();
            break;

        case 'FBServiceDashboard':
            
            HotelRevenueDataChart1(firstButton,'htlissue', 1);
            total_SRMSRequestChart(firstButton,'srms', 1);
            RDGuestMetChart(firstButton,'GMguest', 1);
            TopSRMSrequestChart(firstButton,'topSRMS', 1);
            total_SRMSRequestCompletionChart(firstButton,'totalSRMS', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            dailyBreakageDataChart(firstButton,'breakreport', 1);
            restaurantFeedbackDataChart(firstButton,'feedback', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            MainingGuideChart('mainingGuide');
            DiscardsChartData(firstButton,'discardchart', 1);
            RDEmpResignation();
            FollowUps();
            break;
    

        case 'salesDashboard':
            setDateInputValue();
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData();
            CEORevenueTotalData(firstButton,'CEOData', 1);
            SalesContractChartData(firstButton,'sc', 1);
            DSRChart(firstButton,'dsr',1);
            out_of_orderChart(firstButton,'outoforder', 1);
            RDGuestMetChart(firstButton,'GMguest', 1);
            ArCollectionDatachart(firstButton,'arc', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            forecastDatachart(firstButton, 'occ',1);
            forecastAdrDatachart(firstButton,'adr', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            RDCompRoom();
            MainingGuideChart('mainingGuide');
            RDEmpResignation();
            FollowUps();
            break;
        case 'marketingDashboard':
            setDateInputValue();
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData();
            CEORevenueTotalData(firstButton,'CEOData', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            MainingGuideChart('mainingGuide');
            RDEmpResignation();
            FollowUps();
            break;
        case 'revenueDashboard':
            setDateInputValue();
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData();
            CEORevenueTotalData(firstButton,'CEOData', 1);
            SalesContractChartData(firstButton,'sc', 1);
            out_of_orderChart(firstButton,'outoforder', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            forecastDatachart(firstButton, 'occ',1);
            forecastAdrDatachart(firstButton,'adr', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            MainingGuideChart('mainingGuide');
            RDEmpResignation();
            FollowUps();
            break;
        case 'financeDashboard':
            setDateInputValue();
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData();
            CEORevenueTotalData(firstButton,'CEOData', 1);
            SalesContractChartData(firstButton,'sc', 1);
            out_of_orderChart(firstButton,'outoforder', 1);
            ArCollectionDatachart(firstButton,'arc', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            forecastDatachart(firstButton, 'occ',1);
            forecastAdrDatachart(firstButton,'adr', 1);
            payMasterDatachart(firstButton,'paymaster', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            dailyBreakageDataChart(firstButton,'breakreport', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            RDCapex();
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            RDEmpResignation();
            RDGatepass();
            FollowUps();
            RDCompRoom();
            MainingGuideChart('mainingGuide');
            organizationList();
            break;
        case 'D_OpsDashboard':
            setDateInputValue();
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData();
            CEORevenueTotalData(firstButton,'CEOData', 1);
            forecastDatachart(firstButton, 'occ',1);
            forecastAdrDatachart(firstButton,'adr', 1);
            payMasterDatachart(firstButton,'paymaster', 1);
            out_of_orderChart(firstButton,'outoforder', 1);
            total_SRMSRequestChart(firstButton,'srms', 1);
            RDGuestMetChart(firstButton,'GMguest', 1);
            ArCollectionDatachart(firstButton,'arc', 1);
            PpmRoomsDatachart(firstButton,'PPM', 1);
            TopSRMSrequestChart(firstButton,'topSRMS', 1);
            total_SRMSRequestCompletionChart(firstButton,'totalSRMS', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            maintanceBreakdown(firstButton,'maintance', 1);
            dailyBreakageDataChart(firstButton,'breakreport', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            organizationList();
            RDLeaveApplication();
            RDGatepass();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            MainingGuideChart('mainingGuide');
            RDEmpResignation();
            FollowUps();
            break;
        case 'HRDashboard':
            HotelRevenueDataChart1(firstButton,'htlissue', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            RDEmpResignation();
            RDExitInterview();
            RDPADPList();
            FollowUps();
            MainingGuideChart('mainingGuide');
            break;
        case 'trainingDashboard':
            HotelRevenueDataChart1(firstButton,'htlissue', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            restaurantFeedbackDataChart(firstButton,'feedback', 1);
            ConsumptionDataChart1(firstButton,'csd', 1);
            RDChecklistChartData(firstButton,'checklistloader', 1);
            DiscardsChartData(firstButton,'discardchart', 1);
            LostAndFoundChart(firstButton,'lf', 1);
            RDLeaveApplication();
            RDOpenPosition();
            RDInterviewAssessment();
            MOMList();
            RDEmpResignation();
            RDExitInterview();
            RDPADPList();
            MainingGuideChart('mainingGuide');
            FollowUps();
            break;
    }
    
    
});
async function organizationList() {
    try {
        const selectOrganazation = document.getElementById('Org_HLP');
        const detailResponse = await fetch(`api/CEOORGList/`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
        const detailData = await detailResponse.json();
        selectOrganazation.innerHTML = '';

        detailData.Table.forEach((org, index) => {
            const option = document.createElement('option');
            option.value = org.OrganizationID; 
            option.textContent = org.Organization_name; 

            
            if (index === 0) {
                option.selected = true;
                
            }

            selectOrganazation.appendChild(option);
        });
    
    } catch (error) {
        console.error('Error fetching topSrmsDetailsModal data:', error);
        document.getElementById('topSrmsCompletedDurationDetailsModalBody').innerText = 'Error fetching details.';
    }
   await BindHLPReportChart('hlp');
}

async function HotelRevenueData(){
try {
    const RT= document.getElementById('date_Hotelrevenue').value;

    const detailResponse = await fetch(`api/HotelRevenueChartData/?RT=${RT}`);
    if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

    const detailData = await detailResponse.json();
    const toprequestbody = document.getElementById('tbl_Htl_r_V_b_body');
    function formatToINR(number) {
        return number.toLocaleString('en-IN');
    }


    toprequestbody.innerHTML = ''; 

    detailData.Table.forEach((hotel ,index)=> {
    
    const row = document.createElement('tr');
    row.innerHTML = `
            <td class="text-center">${index + 1}</td>
            <td>${hotel.Hotel}</td>
            <td class="text-center">${formatToINR(hotel.FTD_Budget)}</td>
            <td class="text-center">${formatToINR(hotel.TotalRevenue)}</td>
            <td class="text-center" style="color: ${hotel.FTD_Variance < 0 ? 'red' : 'green'};">
                ${formatToINR(hotel.FTD_Variance)}
            </td>
            <td class="text-center">${formatToINR(hotel.MTD_TotalBudget)}
            </td>
            <td class="text-center">${formatToINR(hotel.MTD_Actual)}</td>
            <td class="text-center">
               
                <span style="color: ${hotel.MTD_TotalVariance < 0 ? 'red' : 'green'};">
                    ${formatToINR(hotel.MTD_TotalVariance)}
                </span>
            </td>
            <td class="text-center">${formatToINR(hotel.YTD_TotalBudget)}
            </td>
            <td class="text-center">${formatToINR(hotel.YTD_Actual)}</td>
            <td class="text-center">
               
                <span style="color: ${hotel.YTD_TotalVariance < 0 ? 'red' : 'green'};">
                    ${formatToINR(hotel.YTD_TotalVariance)}
                </span>
            </td>
        
    `;
toprequestbody.appendChild(row);
});
} catch (error) {
console.error('Error fetching EnqEQMaintanceDetailsModal data:', error);
document.getElementById('EnqEQMaintanceDetailsModalbody').innerText = 'Error fetching details.';
}
}

async function BindHLPReportChart(chartType) {
    showLoader(chartType);
    const chartDom = document.getElementById('hlpRrportChart');
    const hlpChart = echarts.init(chartDom);
    try {
        const OID = document.getElementById('Org_HLP').value;
        const RD = document.getElementById('date_HLP').value;
        const response = await fetch(`api/CEOHLPReportChartData/?RD=${RD}&OID=${OID}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        const { Title, YOD } = data.Table.reduce(
            (acc, item) => {
              if (item.YOD && item.YOD !== "0") { // Ensures YOD is not empty, null, or "0"
                acc.Title.push(item.Title);
                acc.YOD.push(item.YOD);
              }
              return acc;
            },
            { Title: [], YOD: [] }
          );
          const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '5%', right: '5%', top: '10%', bottom: '10%', containLabel: true // Adjusted top for better spacing
            },
            xAxis: {
                type: 'value',  // Change to value for horizontal bar
            },
            yAxis: {
                type: 'category',  // Change to category for horizontal bar
                data: Title,  // Use Title for yAxis
                axisLabel: {
                    interval: 0,
                    fontSize: 9,
                }
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '70%',
                    data: YOD,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'right', // Change position to 'right' for horizontal bars
                        formatter: function (params) {
                            let value = params.value;
                            if (value >= 10000000) {
                                return (value / 10000000).toFixed(0) + 'Cr'; // Crores (for values >= 1 crore)
                            } else if (value >= 100000) {
                                return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(0) + 'K';    // Thousands (for values >= 1 thousand)
                            } else {
                                return value;  // If value is below 1000, show it as it is
                            }
                        }
                    }
                },
            ]
        };

        hlpChart.setOption(option);
    } 
    catch (error) {
        hideLoader(chartType);
        console.error('Error fetching total visit chart data:', error);
    }
}


async function maintanceBreakdown(button,chartType,rangeType){
    showLoader(chartType);
    const chartDomf = document.getElementById('maintenance-chart');
    const mChart = echarts.init(chartDomf);
    const chartDom = document.getElementById('breakdown-chart');
    const breakdownChart = echarts.init(chartDom);
    selectedTimeRange = rangeType;
    updateButtonState(button);

    const RT = rangeType;
    let timeRangeText = '';
    switch (rangeType) {
        case 1:
            timeRangeText = "Yesterday's";
            break;
        case 2:
            timeRangeText = "Weekly";
            break;
        case 3:
            timeRangeText = "Monthly";
            break;
        case 4:
            timeRangeText = "Yearly";
            break;
    }
    try {
        const response = await fetch(`api/maintanceBreakdown/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        totalMaintaceBreakdownData=data.totalMaintaceBreakdownData[0]
        document.getElementById('eq_TotalEq').textContent = totalMaintaceBreakdownData.TotalEq;
        document.getElementById('eq_TotalUW').textContent = totalMaintaceBreakdownData.TotalUW;
        document.getElementById('eq_TotalUA').textContent = totalMaintaceBreakdownData.TotalUA;
        document.getElementById('breakdown-label').textContent = `${timeRangeText} Breakdown`;
        document.getElementById('total-Maintenance').textContent = `Total ${timeRangeText} Maintenance`;
        document.getElementById('eq_TotalBreakdown').textContent = totalMaintaceBreakdownData.TotalBreakdown;
        document.getElementById('eq_TotalBreakdownAmount').textContent = totalMaintaceBreakdownData.TotalBreakdownAmount;
        document.getElementById('eq_TotalMaintenance').textContent = totalMaintaceBreakdownData.TotalMaint;
        document.getElementById('pending-maintace-label').textContent = `${timeRangeText} Pending Maintenance `;
        document.getElementById('eq_PendingMaintenance').textContent = totalMaintaceBreakdownData.TotalMaintPending;
       
       
        const maintancData = data.maintenanceBreakdownData; 
        const axis_data = maintancData.map(item => item.Hotel);
        const Total_maintance = maintancData.map(item => item.Total_maintance)
        const Total_maintance_complete = maintancData.map(item => item.Total_maintance_complete);
        const breakdown_count = maintancData.map(item => item.breakdown_count);
        const breakdown_repaired = maintancData.map(item => item.breakdown_repaired);
        const OrganizationID = maintancData.map(item => item.OrganizationID);
        
        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Number of Maintenance', 'Number of Mainenance Completed']
            },
            grid: {
                left: '5%', right: '5%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: 'Number of Maintenance',
                    type: 'bar',
                    
                    barWidth: '25%',
                    data: Total_maintance,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        fontSize: 10,
                        show: true,
                        position: 'top',
                        
                    }
                },
                {
                    name: 'Number of Mainenance Completed',
                    type: 'bar',
                    
                    barWidth: '25%',
                    data: Total_maintance_complete,
                    itemStyle: { color: '#4D5154' },
                    label: {
                        show: true,
                        position: 'top',
                        fontSize: 10,
                        
                    }
                }
            ]
        };
        const option1 = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Number of Breakdown','Number of Breakdown Repaired']
            },
            grid: {
                left: '5%', right: '5%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Number of Breakdown',
                    type: 'bar',
                    fontSize: 9,
                    barWidth: '25%',
                    data: breakdown_count,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'top',
                        
                    }
                },
                {
                    name: 'Number of Breakdown Repaired',
                    type: 'bar',
                    barWidth: '25%',
                    fontSize: 9,
                    data: breakdown_repaired,
                    itemStyle: { color: '#4D5154' },
                    label: {
                        show: true,
                        
                        position: 'top',
                        
                    }
                }
            ]
        };

        mChart.setOption(option);
        breakdownChart.setOption(option1);
        mChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#EnqEQMaintanceDetailsModal').modal('show');
                showLoader('showTotalmaintance');

                let detailResponse;
                if (params.seriesName === "Number of Maintenance") {
                detailResponse = await fetch(`api/CEOEngineeringTotalMaintenanceDetailsData/?RT=${selectedTimeRange}&OrganizationID=${orgId}`);
                }
                else{
                    detailResponse = await fetch(`api/CEOEngineeringTotalPendingMaintenanceDetailsData/?RT=${RT}&OrganizationID=${orgId}`);
                }
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('EnqEQMaintanceDetailsModalbody');


                toprequestbody.innerHTML = ''; 

                detailData.Table.forEach((detail ,index)=> {
                
                const row = document.createElement('tr');
                row.innerHTML = `
                <td>${index + 1}</td>
                <td >${detail.Hotel} </td>
                <td >${detail.Descriptions}</td>
                <td >${detail.Area}</td>
                <td >${detail.Department} </td>
                <td >${detail.WarrantyEndDate}</td>
                <td >${detail.Status}</td>
                <td >${detail.AMCEndDate}</td>
                <td >${detail.AStatus}</td>
                <td >${detail.MaintenanceDate}</td>
                <td >${detail.MStatus}</td>
                        `;
                    toprequestbody.appendChild(row);
                    });                   
                 hideLoader('showTotalmaintance') 

            } 
            catch (error) {
                hideLoader('showTotalmaintance') 
                console.error('Error fetching topSrmsDetailsModal data:', error);
                document.getElementById('topSrmsCompletedDurationDetailsModalBody').innerText = 'Error fetching details.';
            }
                
        });
        breakdownChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#EnqEQBreakdownDetailsModal').modal('show');
                showLoader('showTotalbreakdown');
                const detailResponse = await fetch(`api/CEOEngineeringTotalBreakdownDetailsData/?RT=${RT}&OrganizationID=${orgId}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('EnqEQBreakdownDetailsModalbody');
                toprequestbody.innerHTML = ''; 
                detailData.Table.forEach((detail ,index)=> {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                    <td>${index + 1}</td>
                    <td >${detail.Hotel} </td>
                    <td >${detail.Descriptions}</td>
                    <td >${detail.Area}</td>
                    <td >${detail.Department} </td>
                    <td >${detail.WarrantyEndDate}</td>
                    <td >${detail.Status}</td>
                    <td >${detail.AMCEndDate}</td>
                    <td >${detail.AStatus}</td>
                    <td >${detail.BreakdownDate}</td>
                    <td >${detail.MStatus}</td>
                    <td >${detail.BreakdownReason}</td>
                    <td >${detail.Amount}</td>
                    `;
                toprequestbody.appendChild(row);
                });
                hideLoader('showTotalbreakdown')      

                                        
                

            } catch (error) {
                hideLoader('showTotalbreakdown')      
                
                console.error('Error fetching topSrmsDetailsModal data:', error);
                document.getElementById('topSrmsCompletedDurationDetailsModalBody').innerText = 'Error fetching details.';
            }
                
        });

    
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }

}

async function HotelRevenueDataChart(button,chartType, rangeType) {
    selectedTimeRange = rangeType;
    updateButtonState(button);
    showLoader(chartType);
    
    const RT = rangeType;
    const chartDomf = document.getElementById('chartContainerARR');
    const charthotel = echarts.init(chartDomf);
    const chartDom = document.getElementById('chartContainerOcc');
    const mdChart = echarts.init(chartDom);

   
    
    try {
        const response = await fetch(`api/hotel-chart-data/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        const hotelChartData = data.HotelChartData; // Process hotel data
        const roomData = data.RoomData[0];
        const axis_data = hotelChartData.map(item => item.hotel_name);
        const ARR = hotelChartData.map(item => item.ARR)
        const RevPar = hotelChartData.map(item => item.RevPar);
        const OCC = hotelChartData.map(item => item.OCC);

        try{
            document.getElementById('CompRoom').textContent = roomData.CompRoom;
        document.getElementById('H_CompRoom').textContent = roomData.H_CompRoom;
        document.getElementById('V_CompRoom').textContent = roomData.V_CompRoom;
        document.getElementById('CompRoomPer').textContent = `${roomData.CompRoomPer}%`;
        document.getElementById('CompRoomProgress').style.width = `${roomData.CompRoomPer}%`;

        document.getElementById('TotalGlitch').textContent = roomData.TotalGlitch;
        document.getElementById('TotalGlitchPer').textContent = `${roomData.TotalGlitchPer}%`;
        document.getElementById('TotalGlitchProgress').style.width = `${roomData.TotalGlitchPer}%`;
        debugger;
        document.getElementById('TotalIncident').textContent = roomData.TotalIncident;
        document.getElementById('TotalIncidentPer').textContent = `${roomData.TotalIncidentPer}%`;
        document.getElementById('TotalIncidentProgress').style.width = `${roomData.TotalIncidentPer}%`;
        }
        catch (error) {
            hideLoader(chartType);
           
        }
        




        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['ARR', 'RevPar']
            },
            grid: {
                left: '5%', right: '5%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  
                    fontSize: 10
                },
                minInterval: 1
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: 'ARR',
                    type: 'bar',
                    fontSize: 9,
                    barWidth: '30%',
                    data: ARR,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            let value = params.value;
                            if (value >= 10000000) {
                                return (value / 10000000).toFixed(0) + 'Cr'; // Crores (for values >= 1 crore)
                            } else if (value >= 100000) {
                                return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(0) + 'K';    // Thousands (for values >= 1 thousand)
                            } else {
                                return value;  // If value is below 1000, show it as it is
                            }
                        }
                    }
                },
                {
                    name: 'RevPar',
                    type: 'bar',
                    barWidth: '30%',
                    data: RevPar,
                    itemStyle: { color: '#4D5154' },
                    label: {
                        show: true,
                        fontSize: 9,
                        position: 'top',
                        formatter: function (params) {
                            let value = params.value;
                            if (value >= 10000000) {
                                return (value / 10000000).toFixed(0) + 'Cr'; // Crores (for values >= 1 crore)
                            } else if (value >= 100000) {
                                return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(0) + 'K';    // Thousands (for values >= 1 thousand)
                            } else {
                                return value;  // If value is below 1000, show it as it is
                            }
                        }
                    }
                }
            ]
        };
        const option1 = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Occupancy']
            },
            grid: {
                left: '5%', right: '5%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,
                    fontSize: 10
                },
                minInterval: 1
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Occupancy',
                    type: 'bar',
                    barWidth: '40%',
                    data: OCC,
                    itemStyle: { color: '#FF902F' }, // Color for occupancy bars
                    label: {
                        show: true,
                        position: 'top',
                        formatter: '{c}%',
                        fontSize: 9,
                    }
                },
            ]
        };


        charthotel.setOption(option);
        mdChart.setOption(option1);

        
    } catch (error) {
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }
}

async function HotelRevenueDataChart1(button,chartType, rangeType) {
    selectedTimeRange = rangeType;
    debugger
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    
    try {
        const response = await fetch(`api/hotel-chart-data/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        const roomData = data.RoomData[0];
        hideLoader(chartType);
        
        document.getElementById('CompRoom').textContent = roomData.CompRoom;
        document.getElementById('H_CompRoom').textContent = roomData.H_CompRoom;
        document.getElementById('V_CompRoom').textContent = roomData.V_CompRoom;
        document.getElementById('CompRoomPer').textContent = `${roomData.CompRoomPer}%`;
        document.getElementById('CompRoomProgress').style.width = `${roomData.CompRoomPer}%`;

        document.getElementById('TotalGlitch').textContent = roomData.TotalGlitch;
        document.getElementById('TotalGlitchPer').textContent = `${roomData.TotalGlitchPer}%`;
        document.getElementById('TotalGlitchProgress').style.width = `${roomData.TotalGlitchPer}%`;

        document.getElementById('TotalIncident').textContent = roomData.TotalIncident;
        document.getElementById('TotalIncidentPer').textContent = `${roomData.TotalIncidentPer}%`;
        document.getElementById('TotalIncidentProgress').style.width = `${roomData.TotalIncidentPer}%`;
       
        
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching glitch and incident data data:', error);
    }
}

async function CEORevenueTotalData(button,chartType,timeRange) {
    updateButtonState(button);
    showLoader(chartType);

    let timeRangeText = '';
    switch (timeRange) {
        case 1:
            timeRangeText = 'Yesterday';
            break;
        case 2:
            timeRangeText = 'Weekly';
            break;
        case 3:
            timeRangeText = 'Monthly';
            break;
        case 4:
            timeRangeText = 'Yearly';
            break;
    }


    fetch(`revenue-data/?time_range=${timeRange}`)
        .then(response => response.json())
        .then(data => {
            hideLoader(chartType);
            document.querySelector('.ibox[data-type="Total Revenue"] .ibox-content h1').innerText = data.TotalREVENUE
            document.querySelector('.ibox[data-type="Room Revenue"] .ibox-content h1').innerText = data.RoomRevenue;
            document.querySelector('.ibox[data-type="FB Revenue"] .ibox-content h1').innerText = data.FBRevenue;
            document.getElementById('adr-revpar').innerText = document.getElementById('adr-revpar').innerText = `${data.ADR}/${data.RevPar}`;;
            document.getElementById('outlet-revenue').innerText = data.RestRevenue;
            document.getElementById('banquet-revenue').innerText = data.BanquetRevenue;

            document.getElementById('total-revenue-label').innerText = timeRangeText;
            document.getElementById('room-revenue-label').innerText = timeRangeText;
            document.getElementById('fb-revenue-label').innerText = timeRangeText;
            document.getElementById('adr-revpar-label').innerText = timeRangeText;
            document.getElementById('outlet-revenue-label').innerText = timeRangeText;
            document.getElementById('banquet-revenue-label').innerText = timeRangeText;

        })
        .catch(error => console.error('Error fetching data:', error));
}



async function total_SRMSRequestCompletionChart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('RoomsSRMSCompletedDurationChart');
    const dpChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/RDRoomsSRMSCompletedDurationChart/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }


        const data = await response.json();
        hideLoader(chartType);
        const CompleteDuration = data.Table.map(item => item.CompleteDuration);

        const TotalRequest = data.Table.map(item => item.TotalRequest);


        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Completed Duration']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: CompleteDuration,
                axisLabel: {
                    interval: 0,
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: TotalRequest,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        dpChart.setOption(option);
        dpChart.RT = RT;
        

        dpChart.on('click', async function (params) {
            if (params.componentType === 'series') {
            try {
                const srmsRequest=params.name
                const RT = dpChart.RT;
                $('#topSrmsCompletedDurationDetailsModal').modal('show');
                showLoader('completeDurationSrms');
                const detailResponse = await fetch(`api/RDRoomsSRMSCompletedDurationDetailsChart/?srmsRequest=${params.name}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('topSrmsCompletedDurationDetailsModalBody');
                toprequestbody.innerHTML = ''; // Clear previous content

                detailData.Table.forEach((detail, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${detail.Hotel}</td>
                    <td>${detail.Location}</td>
                    <td>${detail.CallDescription}</td>
                    <td>${detail.RequestMode}</td>
                    <td>${detail.Remark}</td>
                    <td>${detail.RequestDateTime}</td>
                    <td>${detail.AssignedUserName}</td>
                    <td>${detail.CompleteDateTime}</td>
                    <td>${detail.CompleteBy}</td>
                `;
                toprequestbody.appendChild(row);
                
                });
                hideLoader('completeDurationSrms');

                
               

            } catch (error) {
                hideLoader('completeDurationSrms');
                console.error('Error fetching topSrmsDetailsModal data:', error);
                document.getElementById('topSrmsCompletedDurationDetailsModalBody').innerText = 'Error fetching details.';
            }
                }
        });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }
}

async function TopSRMSrequestChart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);


    const RT = rangeType;
    const chartDom = document.getElementById('srmsrequestchart');
    const topSRMSChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/RDRoomsSRMSTopRequestChart/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
    
        const data = await response.json();
        hideLoader(chartType);
        const CallDescription = data.Table.map(item => item.CallDescription);
        const TotalRequest = data.Table.map(item => item.TotalRequest);
    
        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Top Request']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {  
                type: 'value',
            },
            yAxis: {  
                type: 'category',
                data: CallDescription,
                axisLabel: {
                    interval: 0,
                    fontSize: 10
                }
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '70%',
                    data: TotalRequest,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'right', 
                        fontSize:9,
                        
                        
                    }
                },
            ]
        };
    
        topSRMSChart.setOption(option);
        topSRMSChart.RT = RT;
        topSRMSChart.on('click', async function (params) {
            if (params.componentType === 'series') {
                try {
                    $('#topSrmsDetailsModal').modal('show');
                    showLoader('topsrms');
                    const RT = topSRMSChart.RT;

                    const srmsRequest = params.name;
                    const detailResponse = await fetch(`api/RDRoomsSRMSTopRequestDetailsChart/?srmsRequest=${srmsRequest}&RT=${RT}`);
                    if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
    
                    const detailData = await detailResponse.json();
                    const topSrmsDetailsModalBody = document.getElementById('topSrmsDetailsModalBody');
                    topSrmsDetailsModalBody.innerHTML = ''; // Clear previous content
    
                    detailData.Table.forEach((detail, index) => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${index + 1}</td>
                            <td>${detail.Hotel}</td>
                            <td>${detail.TotalRequest}</td>
                        `;
                        topSrmsDetailsModalBody.appendChild(row);
                    });
    
                    
                    $("#topSrmsDetailsModal #requestTitle").text(srmsRequest);
                    hideLoader('topsrms');
                } catch (error) {
                    hideLoader('topsrms');
                    console.error('Error fetching topSrmsDetailsModal data:', error);
                    document.getElementById('topSrmsDetailsModalBody').innerText = 'Error fetching details.';
                }
            }
        });
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }
    
}



async function PpmRoomsDatachart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('ppmRoom-chart');
    const ppmrRoomChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/RDRoomsPPMChart/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };
        ppmrRoomChart.setOption(option);
        ppmrRoomChart.RT = RT;
        ppmrRoomChart.on('click', async function (params) {
        try {
            const orgId = OrganizationID[params.dataIndex];
            $('#PPMCheckListDetailsModal').modal('show');
            showLoader('ppmloader');
            const RT = ppmrRoomChart.RT;
            const detailResponse = await fetch(`api/CEOPPMCheckListDetailsChartDataSelect/?OrganizationID=${orgId}&RT=${RT}`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const toprequestbody = document.getElementById('PPMCheckListDetailsModalBody');


            toprequestbody.innerHTML = ''; 

            detailData.Table.forEach(detail => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td >${detail.RoomNumber} 
                </td>
                <td >${detail.EntryDate}</td>
                <td >${detail.IsDoneEng}</td>
                <td >${detail.IsDoneHK} 
                </td>
                <td><a class="btn btn-primary" target="_blank" href="${GRedURL}/PPMChecklist/Home/Entry/${detail.EntryID}">View</a></td>

            `;
            toprequestbody.appendChild(row);
            });
            hideLoader('ppmloader') 


        

        } catch (error) {
            hideLoader('ppmloader') 
            console.error('Error fetching PayMasterModal data:', error);
            document.getElementById('PPMCheckListDetailsModalBody').innerText = 'Error fetching details.';
        }
            
    });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}

async function trainingHoursDatachart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('trainingHours-chart');
    const trainingChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEOTrainingHours/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total Training hours']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total Training hours',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };
        trainingChart.setOption(option);
        trainingChart.RT = RT;
        trainingChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#TrainingHoursDetailsModal').modal('show');
                showLoader('trainingLoader');
                const RT = trainingChart.RT;
                const detailResponse = await fetch(`api/TrainingHoursDetails/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('TrainingHoursDetailsModalBody');
                toprequestbody.innerHTML = ''; 
        
                detailData.Table.forEach((detail, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td style="text-align:left">${detail.Topic} 
                        </td>
                        <td style="text-align:left"">${detail.Department}</td>
                        <td style="text-align:center">${detail.NoOfMember}</td>
                        <td style="text-align:center">${detail.TrainingDate} 
                        </td>
                        <td style="text-align:center"">${detail.StartTime}</td>
                        <td style="text-align:center">${detail.EndTime}</td>
        
                `;
                toprequestbody.appendChild(row);
                });
                hideLoader('trainingLoader') 
                
               
                
            } catch (error) {
                hideLoader('trainingLoader') 
                console.error('Error fetching TrainingHoursDetailsModal data:', error);
                document.getElementById('TrainingHoursDetailsModalBody').innerText = 'Error fetching details.';
            }
                    
            });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}


async function RDChecklistChartData(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('checklist-chart');
    const checklistChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/RDChecklistChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);
        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };
        checklistChart.setOption(option);
        checklistChart.RT = RT;

        checklistChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                const RT = checklistChart.RT;
                $('#ChecklistDetailsmodal').modal('show');
                showLoader('checklistLoader');
                const detailResponse = await fetch(`api/RDCheckListDetailsChart/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('ChecklistDetailsmodalbody');
                toprequestbody.innerHTML = ''; 
        
                detailData.Table.forEach((detail, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                     <td style="text-align:left">${index + 1 } 
                        </td>
                    <td style="text-align:left">${detail.Title} 
                        </td>
                        <td style="text-align:left"">${detail.Department}</td>
                        <td style="text-align:left">${detail.EntryDate}</td>
                        <td style="text-align:left">${detail.EntryBy} 
                        </td>
        
                `;
                toprequestbody.appendChild(row);
                });
                hideLoader('checklistLoader') 
        
                
               
                
            } catch (error) {
                hideLoader('checklistLoader') 
                console.error('Error fetching ChecklistDetailsmodal data:', error);
                document.getElementById('ChecklistDetailsmodalbody').innerText = 'Error fetching details.';
            }
                    
            });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}
const ongoingRequests = new Set();
async function warningLettersDatachart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('warningLetterChart');
    const warningLetChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEOWarningLetters/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total Warning Letter']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total Warning Letter',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        warningLetChart.setOption(option);
        warningLetChart.RT = RT;
        warningLetChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                const RT = warningLetChart.RT;
                if (ongoingRequests.has(RT)) {
                    
                    return; 
                }
                ongoingRequests.add(RT);
                $('#WarningLettersDetailsmodal').modal('show');
                showLoader('warningLoader');
                const detailResponse = await fetch(`api/WarningLettersDetails/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('WarningLettersDetailsmodalBody');
                toprequestbody.innerHTML = ''; 
        
                detailData.Table.forEach((detail, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                     <td style="text-align:left">${index + 1 } 
                        </td>
                    <td style="text-align:left">${detail.Name} 
                        </td>
                        <td style="text-align:left"">${detail.Designation}</td>
                        <td style="text-align:left">${detail.Department}</td>
                        <td style="text-align:center">${detail.EmployeeProblems} 
                        </td>
                        <td style="text-align:center"">${detail.WarningType}</td>
                        <td style="text-align:center">${detail.WarnOn}</td>
        
                `;
                toprequestbody.appendChild(row);
                });
                hideLoader('warningLoader') 
                ongoingRequests.delete(RT);
        
                
               
                
            } catch (error) {
                hideLoader('warningLoader') 
                ongoingRequests.delete(RT);
                console.error('Error fetching WarningLettersDetailsmodal data:', error);
                document.getElementById('WarningLettersDetailsmodalBody').innerText = 'Error fetching details.';
            }
                    
            });




    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}



async function cateringSaleDatachart(button, chartType,rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('cateringSale-chart');
    const cateringSaleChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEOCateringSalesEvent/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Daily Catering Sales']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Daily Catering Sales',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        cateringSaleChart.setOption(option);
        cateringSaleChart.RT = RT;
        cateringSaleChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#cateringSalesEventDetailsmodal').modal('show');
                showLoader('cateringLoader');
                const RT = cateringSaleChart.RT;
                const detailResponse = await fetch(`api/CateringSalesEventDetails/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('cateringSalesEventDetailsmodalBody');
                toprequestbody.innerHTML = ''; 
        
                detailData.Table.forEach((detail, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                     <td style="text-align:left">${index + 1 } 
                        </td>
                    <td style="text-align:left">${detail.FunctionName} 
                        </td>
                        <td style="text-align:left"">${detail.CompanyName}</td>
                        <td style="text-align:left">${detail.ContactName}</td>
                        <td style="text-align:center">${detail.Attending} 
                        </td>
                        <td style="text-align:center"">${detail.ArrivalDate}</td>
                        <td style="text-align:center">${detail.DepartureDate}</td>
        
                `;
                toprequestbody.appendChild(row);
                });
                hideLoader('cateringLoader') ;
        
                
                
                
            } catch (error) {
                hideLoader('cateringLoader') ;
                console.error('Error fetching cateringSalesEventDetailsmodal data:', error);
                document.getElementById('cateringSalesEventDetailsmodalBody').innerText = 'Error fetching details.';
            }
                    
            });



    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}

async function dailyBreakageDataChart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('dailyBreakage-chart');
    const breakageChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/DailyBreakageData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total Cost']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total Cost',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        breakageChart.setOption(option);
        breakageChart.RT = RT;
        breakageChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#DailyBreakageDetails').modal('show');
                showLoader('dailyBreakage');
                const RT = breakageChart.RT;
                const detailResponse = await fetch(`api/DailyBreakageDetails/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('DailyBreakageDetailsBody');
                toprequestbody.innerHTML = ''; 
        
                detailData.Table.forEach((detail, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                     <td style="text-align:center">${index + 1 } 
                        </td>
                    <td style="text-align:left">${detail.Item} 
                        </td>
                        <td style="text-align:center"">${detail.Nos}</td>
                        <td style="text-align:center">${detail.TotalCost}</td>
                        <td style="text-align:left">${detail.PersonResponsible} 
                        </td>
                        
        
                `;
                toprequestbody.appendChild(row);
                });

                hideLoader('dailyBreakage') 
        
                
                
                
            } catch (error) {
                hideLoader('dailyBreakage') 
                console.error('Error fetching DailyBreakageDetails data:', error);
                document.getElementById('DailyBreakageDetailsBody').innerText = 'Error fetching details.';
            }
                    
            });



    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}

async function restaurantFeedbackDataChart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('restaurantFeedback-chart');
    const restaurantFeedbackChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/restaurantFeedbackChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        restaurantFeedbackChart.setOption(option);
        restaurantFeedbackChart.RT = RT;
        restaurantFeedbackChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#feedbackDetailsModal').modal('show');
                showLoader('feedbackLoader');
                const RT = restaurantFeedbackChart.RT;
                const detailResponse = await fetch(`api/CEO_RestaurantFeedbackDetails/?OrganizationID=${orgId}&RT=${RT}`);

                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

                
                const detailDataArray = await detailResponse.json();
                const feedbackCategoriesContainer = document.getElementById('feedbackCategories');

                
                feedbackCategoriesContainer.innerHTML = '';

               
                detailDataArray.forEach(detailData => {
                    
                    const feedbackSection = document.createElement('div');
                    feedbackSection.classList.add('feedback-item', 'col-md-12'); 

                    
                    const overallExperience = document.createElement('h5');
                    overallExperience.textContent = `Overall Experience: ${detailData.OverallExperienceComments || 'N/A'}`; 
                    
                    const visitDate = document.createElement('p');
                    visitDate.textContent = `Visit Date: ${detailData.VisitDate || 'N/A'}`;

                    feedbackSection.appendChild(overallExperience);
                    feedbackSection.appendChild(visitDate);

                    
                    const categories = JSON.parse(detailData.Column1);
                    
                    categories.forEach(category => {
                        const categoryDiv = document.createElement('div');
                        categoryDiv.classList.add('mb-3');

                        const categoryTitle = `<h6><strong>${category.Category}</strong></h6>`;
                        categoryDiv.innerHTML += categoryTitle;

                        
                        const table = document.createElement('table');
                        table.classList.add('table', 'table-bordered', 'table-sm');

                        const thead = document.createElement('thead');
                        thead.innerHTML = '<tr><th>Attribute</th><th>Response</th></tr>';
                        table.appendChild(thead);

                        const tbody = document.createElement('tbody');

                        category.b.forEach(attribute => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td><strong>${attribute.Attribute}</strong></td>
                                <td>${attribute.AD.length > 0 ? attribute.AD.map(a => a.Answer).join(', ') : 'N/A'}</td>
                            `;
                            tbody.appendChild(row);
                        });

                        table.appendChild(tbody);
                        categoryDiv.appendChild(table);

                        
                        feedbackSection.appendChild(categoryDiv);
                    });

                    
                    feedbackCategoriesContainer.appendChild(feedbackSection);
                });
                hideLoader('feedbackLoader') 

                
                

                
            } catch (error) {
                hideLoader('feedbackLoader') 
                console.error('Error fetching DailyBreakageDetails data:', error);
                document.getElementById('DailyBreakageDetailsBody').innerText = 'Error fetching details.';
            }
                    
            });



    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}

async function ConsumptionDataChart(button,chartType,rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('consumptionchart');
    const consumptionChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEODashboardConsumptionChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        consumptionChart.setOption(option);
        consumptionChart.RT = RT;
        consumptionChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#consumptionDetails').modal('show');
                showLoader('consumption');
                const RT = consumptionChart.RT;

                const detailResponse = await fetch(`api/CEO_ConsumptionDetailsChartDataSelect/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('consumptionDetailsBody');
                toprequestbody.innerHTML = ''; 
        
                detailData.Table.forEach((detail, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                     <td style="text-align:center">${index + 1 } 
                        </td>
                    <td style="text-align:left">${detail.Con_Date} 
                        </td>
                        <td style="text-align:center"">${detail.ItemCode}</td>
                        <td style="text-align:center">${detail.Item}</td>
                        <td style="text-align:left">${detail.Department} 
                        </td>
                         <td style="text-align:center">${detail.Store } 
                        </td>
                    <td style="text-align:left">${detail.Quantity} 
                        </td>
                        <td style="text-align:center"">${detail.Rate}</td>
    
                        <td style="text-align:left">${detail.TotalAmount} 
                        </td>
                        
        
                `;
                toprequestbody.appendChild(row);
                });
                hideLoader('consumption') 
        
                
                
                
            } catch (error) {
                hideLoader('consumption') ;
                console.error('Error fetching consumptionDetails data:', error);
                document.getElementById('consumptionDetailsBody').innerText = 'Error fetching details.';
            }
                    
            });



    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}



async function ConsumptionDataChart1(button,chartType,rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('consumptionchart');
    const consumptionChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/RDDashboardConsumptionChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        consumptionChart.setOption(option);
        consumptionChart.RT = RT;
        consumptionChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                const RT = consumptionChart.RT;
                const detailResponse = await fetch(`api/RD_ConsumptionDetailsChartDataSelect/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('consumptionDetailsBody');
                toprequestbody.innerHTML = ''; 
        
                detailData.Table.forEach((detail, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                     <td style="text-align:center">${index + 1 } 
                        </td>
                    <td style="text-align:left">${detail.Con_Date} 
                        </td>
                        <td style="text-align:center"">${detail.ItemCode}</td>
                        <td style="text-align:center">${detail.Item}</td>
                        <td style="text-align:left">${detail.Department} 
                        </td>
                         <td style="text-align:center">${detail.Store } 
                        </td>
                    <td style="text-align:left">${detail.Quantity} 
                        </td>
                        <td style="text-align:center"">${detail.Rate}</td>
    
                        <td style="text-align:left">${detail.TotalAmount} 
                        </td>
                        
        
                `;
                toprequestbody.appendChild(row);
                });
        
                
                $('#consumptionDetails').modal('show');
                
            } catch (error) {
                console.error('Error fetching consumptionDetails data:', error);
                document.getElementById('consumptionDetailsBody').innerText = 'Error fetching details.';
            }
                    
            });



    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}

async function RDGuestMetChart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('guestMet');
    const guestChart = echarts.init(chartDom);

    try {
        const response = await fetch(`api/RDGuestMetChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);
        const OrganizationID = data.Table.map(item => item.OrganizationID)
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);
        const TotalArrival = data.Table.map(item => item.TotalArrival === 0 ? null : item.TotalArrival);
        const TotalDeparture = data.Table.map(item => item.TotalDeparture === 0 ? null : item.TotalDeparture);
        const TotalInHouse = data.Table.map(item => item.TotalInHouse === 0 ? null : item.TotalInHouse);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total', 'Arrival', 'Departure', 'In-house']
            },
            grid: {
                left: '5%',
                right: '5%',
                bottom: '15%',
                containLabel: true,
            },
            xAxis: {
                type: 'category',
                data: axis_data,  // Hotel names
                axisLabel: {
                    interval: 0,
                    fontSize: 10,
                    formatter: function (value) {
                        return value.length > 5 ? value.slice(0, 5) + '...' : value;
                    }
                }
            },
            yAxis: {
                type: 'value',
                name: 'Guest Count'
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    data: Total,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === 0 ? '' : params.value;
                        },
                        textStyle: {
                            fontSize: 10,
                            color: '#000'
                        }
                    },
                    barWidth: '25%'
                },
                {
                    name: 'Arrival',
                    type: 'bar',
                    data: TotalArrival,
                    itemStyle: { color: 'rgb(140,217,201)' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === 0 ? '' : params.value;
                        },
                        textStyle: {
                            fontSize: 10,
                            color: '#000'  // Black color for labels
                        }
                    },
                    barWidth: '20%'
                },
                {
                    name: 'Departure',
                    type: 'bar',
                    data: TotalDeparture,
                    itemStyle: { color: 'rgb(238, 164, 127)' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === 0 ? '' : params.value;
                        },
                        textStyle: {
                            fontSize: 10,
                            color: '#000'
                        }
                    },
                    barWidth: '20%'
                },
                {
                    name: 'In-house',
                    type: 'bar',
                    data: TotalInHouse,
                    itemStyle: { color: 'rgb(131, 163, 247)' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === 0 ? '' : params.value;
                        },
                        textStyle: {
                            fontSize: 10,
                            color: '#000'
                        }
                    },
                    barWidth: '20%'
                }
            ]
        };


        guestChart.setOption(option);
        guestChart.RT = RT;
        guestChart.on('click', async function (params) {
                try {
                    const orgId = OrganizationID[params.dataIndex];
                    const MetOn = params.seriesName
                    const RT = guestChart.RT;
                    
                    const detailResponse = await fetch(`api/RDGuestMetChartDataDetails/?OrganizationID=${orgId}&RT=${RT}&MetOn=${MetOn}`);
                    if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

                    const detailData = await detailResponse.json();
                    const toprequestbody = document.getElementById('GuestMetDetailsbody');
                    toprequestbody.innerHTML = ''; 

                    detailData.Table.forEach((detail, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td  style="width:70px">${index + 1}</td>
                        <td style="width:170px">${detail.GuestName} <br>${detail.RoomNo}
                        </td>
                        <td>${detail.Arrival}<br>${detail.Departure}</td>
                        <td>${detail.Feedback}</td>
                        <td>${detail.Actiontaken}</td>
                        <td>${detail.FeedbackType}</td>
                        <td>${detail.MetOn}<br>${detail.MetBy}</td>
                        <td>${detail.Updatedby}</td>
                        <td>${detail.UpdateOn}</td>

                    `;
                    toprequestbody.appendChild(row);
                    });

                    
                            $('#GuestMetDetails').modal('show');
                    
                } catch (error) {
                    console.error('Error fetching GuestMetDetails data:', error);
                    document.getElementById('GuestMetDetailsbody').innerText = 'Error fetching details.';
                }
                        
                });
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching total visit chart data:', error);
    }
}





async function total_SRMSRequestChart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('chartOfSRMSRequest');
    const srmsChart = echarts.init(chartDom);

    try {
        const response = await fetch(`api/RDRoomsSRMSChart/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);
       
        const detailsMapping = {};
        data.Table.forEach(item => {
            detailsMapping[item.Hotel] = item.DetailsJson; // Map the DetailsJson to the corresponding hotel
             });

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        srmsChart.setOption(option);
        srmsChart.on('click', function (params) {
        if (params.componentType === 'series') {
            const clickedHotel = params.name; 
            const detailsJson = detailsMapping[clickedHotel]; 
            // const chartType = 'totalsrms';

        
            $('#totalSRMSDetailsModal').modal('show');
            showLoader('totalsrms');


            if (detailsJson) {
                const detailsArray = JSON.parse(detailsJson); 
            
                const tableBody = document.getElementById('totalSRMSrequestDetailsBody');
                tableBody.innerHTML = ''; 

                detailsArray.forEach((detail, index) => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td>${detail.Location}</td> 
                        <td>${detail.CallDescription}</td> 
                        <td>${detail.Department || ''}</td>
                        <td>${detail.RequestMode || ''}</td>
                        <td>${detail.RequestOn || ''}</td>
                        <td>${detail.Status || ''}</td>
                        <td>${detail.AssignedUserName || ''}</td>
                        <td>${detail.CompletedOn || ''}</td>
                        <td>${detail.CompleteDurestion || ''} Mins</td>
                    `;
                    tableBody.appendChild(row);
                    
                });

                
                
            }
            hideLoader('totalsrms');
           
        }
    });
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching sale chart data:', error);
    }
}

function updateButtonState(button) {
    const buttons = button.parentNode.querySelectorAll('button');
    buttons.forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-default');
    });
    button.classList.remove('btn-default');
    button.classList.add('btn-primary');
}

async function out_of_orderChart(button,chartType, rangeType) {
    
    updateButtonState(button);
    const RT = rangeType;
    const Selected_RT=rangeType;
    const chartDom = document.getElementById('chartoutoforder');
    const outOfOrderChart = echarts.init(chartDom);
    showLoader(chartType);

    try {
        
        const response = await fetch(`api/CEOOutOfOrderData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        const axis_data = data.Table.map(item => item.Hotel);
        const OrganizationID = data.Table.map(item => item.OrganizationID)
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);
        hideLoader(chartType);


        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };

       
        outOfOrderChart.setOption(option);
        outOfOrderChart.RT = RT;
        outOfOrderChart.on('click', async function (params) {
        if (params.componentType === 'series') {
            const orgId = OrganizationID[params.dataIndex]; // Get OrganizationID based on the clicked bar
            const Selected_RT = outOfOrderChart.RT;
            await openModal(orgId,Selected_RT); // Open modal with Organization ID
        }
        });
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }
}

async function openModal(orgId,RT) {
    const chartType='outofloader'
    try {
        $('#OutOfOrderModal').modal('show');
        showLoader(chartType);
        const detailResponse = await fetch(`api/CEOOutOfOrderDetails/?OrganizationID=${orgId}&RT=${RT}`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

        const detailData = await detailResponse.json();
        const detailContent = document.getElementById('detailContent');
        detailContent.innerHTML = ''; // Clear previous content

        detailData.OutOfOrderDetailsData.forEach((detail, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${detail.ROMNUB}</td>
            <td>${detail.FRMDAT}</td>
            <td>${detail.TOODAT}</td>
            <td>${detail.DESCRP}</td>
        `;
        detailContent.appendChild(row);
       
        });
        hideLoader(chartType);

        
       

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching CEOOutOfOrderDetails data:', error);
        document.getElementById('detailContent').innerText = 'Error fetching details.';
    }
}



async function DSRChart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('chartOfTotalVisit');
    const mdChart = echarts.init(chartDom);

    try {
        const response = await fetch(`api/RDDSRChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);
        const total_visit = data.Table.map(item => item.TotalVisit === 0 ? null : item.TotalVisit);
        

        const detailsMapping = {};
        data.Table.forEach(item => {
            detailsMapping[item.Hotel] = item.DetailsJson; 
             });
          

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total Visit']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total Visit',
                    type: 'bar',
                    barWidth: '25%',
                    data: total_visit,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === null ? '' : params.value;  // Don't display 0 labels
                        }
                    }
                },
            ]
        };

        mdChart.setOption(option);
       
        mdChart.on('click', function (params) {
        if (params.componentType === 'series') {
        
        const clickedHotel = params.name; 
        const totalVisit = params.value;
        const detailsJson = detailsMapping[clickedHotel]; 
        const chartType='dsrchart';
        $('#dsrDetails').modal('show');
        showLoader(chartType);
        document.getElementById('modalDSRHotelName').textContent = clickedHotel; // Update hotel name
        document.getElementById('modalDSRTotalVisit').textContent = totalVisit;
        
        if (detailsJson) {
            const detailsArray = JSON.parse(detailsJson); 
         
            const tableBody = document.getElementById('dsrdetailContent');
            tableBody.innerHTML = '';

            detailsArray.forEach((detail,index) => {
                const companyDetailsArray = detail.am;

                companyDetailsArray.forEach(companyDetails=> {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td>${companyDetails.CompanyName || ''}</td>
                        <td>${companyDetails.ContactName || ''}</td>
                        <td>${detail.CommunicationMode || ''}</td>
                        <td>${detail.FIT || ''}</td>
                        <td>${detail.GuestResponse || ''}</td>
                        <td>${detail.VisitDate || ''}</td>
                        <td>${detail.NextFollowUpDate || ''}</td>
                        <td>${detail.Remarks || ''}</td>
                        <td>${detail.Username || ''}</td>
                    `;
                    tableBody.appendChild(row);
                });
            });
           
            
            
        }
        hideLoader(chartType);
        }
        });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching total visit chart data:', error);
    }
}


async function forecastDatachart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('forecast-occupancy');
    const forecastChart = echarts.init(chartDom);

    try {
        const response = await fetch(`api/HotelForecastOccupancyChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);
        const Occupancy = data.Table.map(item => item.Occupancy === 0 ? null : item.Occupancy);
        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Occupancy',
                    type: 'bar',
                    barWidth: '25%',
                    data: Occupancy,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: '{c}%',
                        fontSize: 9
                        
                    }
                },
            ]
        };

        forecastChart.setOption(option);
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching total visit chart data:', error);
    }
}


async function forecastAdrDatachart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('adr-chart');
    const forcastAdrChart = echarts.init(chartDom);

    try {
        const response = await fetch(`api/HotelForecastADRChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);
        const ADR = data.Table.map(item => item.ADR === 0 ? null : item.ADR);
        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'ADR',
                    type: 'bar',
                    barWidth: '25%',
                    data: ADR,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === null ? '' : params.value;  // Don't display 0 labels
                        }
                    }
                },
            ]
        };

        forcastAdrChart.setOption(option);
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching total visit chart data:', error);
    }
}

async function payMasterDatachart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('payMaster-chart');
    const paymasterChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEOPayMasterChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const balance = data.Table.map(item => item.balance === 0 ? null : item.balance);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: balance,
                    itemStyle: { color: '#FF902F' },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            let value = params.value;
                            if (value >= 10000000) {
                                return (value / 10000000).toFixed(1) + 'Cr'; // Crores (for values >= 1 crore)
                            } else if (value >= 100000) {
                                return (value / 100000).toFixed(1) + 'L';  // Lakhs (for values >= 1 lakh)
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'k';    // Thousands (for values >= 1 thousand)
                            } else {
                                return value;  // If value is below 1000, show it as it is
                            }
                        }
                    }
                },
            ]
        };


        paymasterChart.setOption(option);
        paymasterChart.RT = RT;
        paymasterChart.on('click', async function (params) {
        try {
            const orgId = OrganizationID[params.dataIndex];
            $('#PayMasterModal').modal('show');
            showLoader('payloader');
            const RT = paymasterChart.RT;
            const detailResponse = await fetch(`api/GMPayMaster/?OrganizationID=${orgId}&RT=${RT}`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const toprequestbody = document.getElementById('PayMasterModalBody');


            toprequestbody.innerHTML = ''; 

            detailData.Table.forEach(detail => {
            document.getElementById('sp_PayMaster_LastupdateDate').textContent=detail.LastupdateDate
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="text-align:left">${detail.ROOM} 
                </td>
                <td style="text-align:left"">${detail.FULL_NAME}</td>
                <td style="text-align:left">${detail.COMPANY_NAME}</td>
                <td style="text-align:center">${detail.ARRIVAL} 
                </td>
                <td style="text-align:center"">${detail.DEPARTURE}</td>
                <td style="text-align:right">${detail.BALANCE}</td>

            `;
            toprequestbody.appendChild(row);
            });
            hideLoader('payloader')

           
        
        } catch (error) {
            hideLoader('payloader')
            console.error('Error fetching PayMasterModal data:', error);
            document.getElementById('PayMasterModalBody').innerText = 'Error fetching details.';
        }
            
    });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}

async function SalesContractChartData(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('chartContainer');
    const saleChart = echarts.init(chartDom);

    try {
        const response = await fetch(`api/RDSalesContractChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);
        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);
        const TotalActive = data.Table.map(item => item.TotalActive === 0 ? null : item.TotalActive);
        const TotalExpired = data.Table.map(item => item.TotalExpired === 0 ? null : item.TotalExpired);
        const DetailsJson = data.Table.map(item => item.DetailsJson === 0 ? null : item.DetailsJson);
        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total', 'Active', 'Expired'] 
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
                name: 'Contracts'
            },
            series: [
                {
                    name: 'Total',  // Add Total series
                    type: 'bar',
                    barWidth: '25%',  // Set width for the bar
                    data: Total,
                    itemStyle: { color: '#FF902F' },  // Color for total contracts
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === null ? '' : params.value;
                        }
                    }
                },
                
                {
                    name: 'Active',  // Active series
                    type: 'bar',
                    barWidth: '25%',  // Set width for the bar
                    data: TotalActive,
                    itemStyle: { color: 'rgb(140,217,201)' },  // Color for active contracts
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === null ? '' : params.value;
                        }
                    }
                },
                {
                    name: 'Expired',  // Expired series
                    type: 'bar',
                    barWidth: '25%',  // Set width for the bar
                    data: TotalExpired,
                    itemStyle: { color: 'rgb(238,164,127)' } , // Color for expired contracts
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            return params.value === null ? '' : params.value;
                        }
                    }
                }
            ]
        };
        saleChart.setOption(option);
        saleChart.RT = RT;
        saleChart.on('click', async function (params) {
        if (params.componentType === 'series') {
        const orgId = OrganizationID[params.dataIndex]; 
            const status = params.seriesName; 
            const RT = saleChart.RT; 
            salechartDetailsModal(orgId,RT,status)
        }
        });
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching sale chart data:', error);
    }
}   

async function salechartDetailsModal(orgId,RT,status) {
    try {
        const detailResponse = await fetch(`api/RDSalesContractChartDataDetails/?OrganizationID=${orgId}&RT=${RT}&status=${status}`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

        const detailData = await detailResponse.json();
        const salesContactDetailsbody = document.getElementById('salesContactDetailsbody');
        salesContactDetailsbody.innerHTML = ''; // Clear previous content

        detailData.saleChartDetailsData.forEach((detail, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${detail.CompanyName}</td>
            <td>${detail.VendorName}</td>
            <td>${detail.FromDate}</td>
            <td>${detail.ToDate}</td>
            <td>${detail.UploadStatus}</td>
            <td>${detail.AccountManager}</td>
            <td>${detail.CreditApproved}</td>
        `;
        salesContactDetailsbody.appendChild(row);
        });

        
        $('#salesContactDetails').modal('show');

    } catch (error) {
        console.error('Error fetching CEOOutOfOrderDetails data:', error);
        document.getElementById('salesContactDetailsbody').innerText = 'Error fetching details.';
    }
}
async function ArCollectionDatachart(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('ArCollection-chart');
    const ArcollectionChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEOARCollectionChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.Table.map(item => item.Hotel);

        const OrganizationID = data.Table.map(item => item.OrganizationID);
        const balance = data.Table.map(item => item.balance === 0 ? null : item.balance);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: balance,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            let value = params.value;
                            if (value >= 10000000) {
                                return (value / 10000000).toFixed(1) + 'Cr'; // Crores (for values >= 1 crore)
                            } else if (value >= 100000) {
                                return (value / 100000).toFixed(1) + 'L';  // Lakhs (for values >= 1 lakh)
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'k';    // Thousands (for values >= 1 thousand)
                            } else {
                                return value;  // If value is below 1000, show it as it is
                            }
                        }
                    }
                },
            ]
        };


        ArcollectionChart.setOption(option);
        ArcollectionChart.RT = RT;
        ArcollectionChart.on('click', async function (params) {
        try {
            let totalDay91 = 0; 
            let totalPending = 0; 
            const orgId = OrganizationID[params.dataIndex];
            const RT = ArcollectionChart.RT;
            
            $('#ARCollectionModal').modal('show');
            showLoader('ARCollectionLoader');
            const detailResponse = await fetch(`api/GMArCollection/?OrganizationID=${orgId}&RT=${RT}`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const toprequestbody = document.getElementById('ARCollectionModalBody');


            toprequestbody.innerHTML = ''; 

            detailData.Table.forEach((detail,index) => {
            document.getElementById('sp_arC_LastupdateDate').textContent=detail.LastupdateDate
            const day91Value = parseFloat(detail.Day91.replace(/,/g, '')); 
            const totalPendingValue = parseFloat(detail.TotalPending.replace(/,/g, '')); 

            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="width:50px">${index + 1} 
                </td>
                <td style="width:170px">${detail.Account} 
                </td>
                <td style="text-align:right">${detail.Day91}</td>
                <td style="text-align:right">${detail.TotalPending}</td>

            `;
            toprequestbody.appendChild(row);
            totalDay91 += day91Value; 
            totalPending += totalPendingValue; 
            });
            const totalRow = document.createElement('tr');
            totalRow.innerHTML = `
                <td colspan="2" style="text-align:center; font-weight:bold">Total:</td>
                <td style="text-align:right; font-weight:bold">${totalDay91.toLocaleString('en-IN')}</td> 
                <td style="text-align:right; font-weight:bold">${totalPending.toLocaleString('en-IN')}</td>
            `;
            toprequestbody.appendChild(totalRow);

            hideLoader('ARCollectionLoader')

            
                   
        
        } catch (error) {
            hideLoader('ARCollectionLoader')
            console.error('Error fetching ARCollectionModal data:', error);
            document.getElementById('ARCollectionModalBody').innerText = 'Error fetching details.';
        }    
        });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching ARCollection   data:', error);
    }
}


async function CEODashboardMasterData(){
    try{
        const detailResponse = await fetch(`api/CEODashboardMasterData`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
           
            


            
            const capexTotalCount = detailData.Capex.length;
            const leaveListCount = detailData.LeaveApplication.length;
            const OpenPositionsCount = detailData.OpenPosition.length;
            const IAListCount = detailData.InterviewAssessment.length;
            const ResignListCount = detailData.EmpResignation.length;
            const exitInterviewListCount = detailData.exitInterview.length;
            const CompRoomListCount = detailData.CompRoom.length;
            const PADPListCount = detailData.PADP.length;
            document.getElementById('capexListCount').textContent = capexTotalCount;
            document.getElementById('leaveListCount').textContent = leaveListCount;
            document.getElementById('OpenPositionsCount').textContent = OpenPositionsCount;
            document.getElementById('IAListCount').textContent = IAListCount;
            document.getElementById('ResignListCount').textContent = ResignListCount;
            document.getElementById('exitInterviewListCount').textContent = exitInterviewListCount;
            document.getElementById('CompRoomListCount').textContent = CompRoomListCount;
            document.getElementById('PADPListCount').textContent = PADPListCount;


            const capexBody = document.getElementById('capexBody');
            capexBody.innerHTML = ''; 
            detailData.Capex.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `viewCapex(this, ${detail.ID}, ${detail.A_Q_GM}, ${detail.OrganizationID})`);
            row.style.cursor = 'pointer';
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                        ${detail.Item}<br>

                    </td>
                    <td>${detail.Qty} </td>
                    <td>${detail.Rate}<br><b>${detail.Total}</b> </td>
            `;
            capexBody.appendChild(row);
            });


            const leaveApplicationBody = document.getElementById('leaveApplicationBody');
            leaveApplicationBody.innerHTML = ''; 
            detailData.LeaveApplication.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `viewLeave(this, ${detail.id},${detail.OrganizationID},"${detail.LeaveType}","${detail.LeaveFrom}", "${detail.LeaveTo}", "${detail.Reason}")`);
            row.style.cursor = 'pointer';
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                        ${detail.EmpName}

                    </td>
                    <td>${detail.LeaveFrom} </td>
                    <td>${detail.LeaveTo}</td>
            `;
            leaveApplicationBody.appendChild(row);
            });




            const PADPListBody = document.getElementById('PADPListBody');
            PADPListBody.innerHTML = ''; 
            detailData.PADP.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `viewPADP(this, ${detail.ID},${detail.UserID},${detail.OrganizationID},"${detail.RT}")`);
            row.style.cursor = 'pointer';
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                       ${detail.EmployeeName} <br>

                    </td>
                    <td>
                    ${detail.SalaryIncrementOption.includes('%') 
                        ? `<span> ${detail.SalaryIncrementOption}</span>`
                        : `<span><b><u>Salary Correction</u></b></span>
                    <br>
                    <span><b style="display: inline-block;min-width:50px">From:</b>${detail.SalaryCorrectionFrom}</span>
                    <span> / <b style="display: inline-block;min-width:50px">To:</b>${detail.SalaryCorrection}</span>`}
                    
                    
                    
                     </td>
                   
            `;
            PADPListBody.appendChild(row);
            });


            

            const OpenPositionsBody = document.getElementById('OpenPositionsBody');
            OpenPositionsBody.innerHTML = ''; 
            detailData.OpenPosition.forEach(detail => {
            const row = document.createElement('tr');
            row.innerHTML = `
                    <td style="text-align:left">${detail.Location} </td>
                    <td>
                        ${detail.Position}

                    </td>
                    <td>${detail.Openedon} </td>
                   
            `;
            OpenPositionsBody.appendChild(row);
            });

           

            const IAListBody = document.getElementById('IAListBody');
            IAListBody.innerHTML = ''; 
            detailData.InterviewAssessment.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `viewIA(this, ${detail.ID},${detail.OrganizationID})`);
            row.style.cursor = 'pointer';
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                        ${detail.Name}

                    </td>
                    <td>${detail.position} </td>
                   
            `;
            IAListBody.appendChild(row);
            });


           



            const ResignListBody = document.getElementById('ResignListBody');
            ResignListBody.innerHTML = ''; 
            detailData.EmpResignation.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `ViewResign(this, ${detail.ID},${detail.OrganizationID})`);
            row.setAttribute('data-name', detail.Name);
            row.setAttribute('data-designation',detail.Designation);
            row.setAttribute('data-department', detail.Department);
            row.setAttribute('data-ResDate', detail.ResDate);
            row.setAttribute('data-emp_code', detail.Emp_Code);
            row.setAttribute('data-DOJ', detail.DOJ);
            row.setAttribute('data-typeofres', detail.TypeofRes);
            row.setAttribute('data-noticeperiod', detail.NoticePeriod);
            row.setAttribute('data-res_reason', detail.Res_Reason);
            row.setAttribute('data-ressubmittedto',detail.Ressubmittedto);
            row.setAttribute('data-lastworkingdays', detail.LastWorkingDays);
            row.setAttribute('data-res_acceptance_date',detail.Res_acceptance_Date);
            row.setAttribute('data-res_acceptance_by', detail.Res_acceptance_By);
            row.style.cursor = 'pointer';

            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                      <strong>  ${detail.Name} </strong><br> ${detail.Designation}

                    </td>
                    <td>${detail.ResDate} </td>
                   
            `;
            ResignListBody.appendChild(row);
            });

            const exitInterviewbody = document.getElementById('exitInterviewBody');
            exitInterviewbody.innerHTML = '';
            detailData.exitInterview.forEach(detail => {
                const row = document.createElement('tr');
                row.setAttribute('onclick', `ViewExitForm(this, ${detail.Exitid},${detail.OrganizationID})`);
                row.style.cursor = 'pointer';
                row.innerHTML = `
                    <td style="text-align:left"">${detail.Hotel}</td>
                    <td style="text-align:center"><strong>${detail.EmpName}</strong> <br> ${detail.Position}
                    </td>
                    <td style="text-align:left">${detail.FinalComment} 
                    </td>
    
                `;
                exitInterviewbody.appendChild(row);
                });


            const CompRoomListBody = document.getElementById('CompRoomListBody');
            CompRoomListBody.innerHTML = ''; 
            detailData.CompRoom.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `ViewCompForm(this, ${detail.CompID})`);
            row.style.cursor = 'pointer';
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                      <b>  ${detail.GuestName} </b><br> ${detail.CompanyName}

                    </td>
                    <td>${detail.PendingSince} </td>
                   
            `;
            CompRoomListBody.appendChild(row);
            });



        }
        catch{

        }
}

async function MOMList(){
    try{
        const detailResponse = await fetch(`api/MOMList`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const MOMListCount = detailData.length;
            document.getElementById('MOMListCount').textContent = MOMListCount;
            const MOMListBody = document.getElementById('MOMListBody');


            MOMListBody.innerHTML = ''; 

            detailData.forEach(detail => {
           
            const row = document.createElement('tr');
            row.setAttribute('onclick', `ViewMOMDetails(this, ${detail.MeetingID})`);
            row.style.cursor = 'pointer';
            row.innerHTML = `
                <td style="text-align:left; background-color: rgb(243,243,244); margin-bottom: 2px; border-bottom: 2px solid white;"><a href="#">${detail.Hotel}</a>  ${detail.Title} 
                </td>
               
               
            `;
            MOMListBody.appendChild(row);
            });

        }
        catch{

        }
}

ViewMOMDetails = function (t, e) {
    $(".MOMDetailsModal").modal("show"), $(".MOMDetailsModal iframe").attr("src", GRedURL+"/MOM/Home/MOMView?M=" + e + "&s=pd");
};

ViewResign = function (t) {
    $(".ViewResignModal").modal("show");
    var e = $(t).attr("data-name");
    $(".ViewResignModal td#Name").text(e);
    var o = $(t).attr("data-emp_code");
    $(".ViewResignModal td#Emp_Code").text(o);
    var n = $(t).attr("data-DOJ");
    $(".ViewResignModal td#DOJ").text(n);
    var l = $(t).attr("data-ResDate");
    $(".ViewResignModal td#ResDate").text(l);
    var d = $(t).attr("data-department");
    $(".ViewResignModal td#Department").text(d);
    var s = $(t).attr("data-designation");
    $(".ViewResignModal td#Designation").text(s);
    var r = $(t).attr("data-typeofres");
    $(".ViewResignModal td#TypeofRes").text(r);
    var i = $(t).attr("data-noticeperiod");
    $(".ViewResignModal td#NoticePeriod").text(i);
    var p = $(t).attr("data-res_reason");
    $(".ViewResignModal td#Res_Reason").text(p);
    var c = $(t).attr("data-ressubmittedto");
    $(".ViewResignModal td#Ressubmittedto").text(c);
    var m = $(t).attr("data-lastworkingdays");
    $(".ViewResignModal td#LastWorkingDays").text(m);
    var u = $(t).attr("data-res_acceptance_date");
    $(".ViewResignModal td#Res_acceptance_Date").text(u);
    var h = $(t).attr("data-res_acceptance_by");
    $(".ViewResignModal td#Res_acceptance_By").text(h);
};


ViewCompForm = function (t,e) {
    $(".CompFormModal .modal-footer").empty(), $(".CompFormModal").modal("show"), $(".CompFormModal iframe").attr("src",GRedURL+"/CompRoom/Home/ViewDetails?VID=" + e);
};


async function FollowUps(){
    try{
        const detailResponse = await fetch(`api/FollowUps`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();


            document.getElementById('followups').innerHTML = '';

            detailData.Table.forEach(detail => {
           
            const li = document.createElement('li');
            li.className = `f_w_l_${detail.FollowUpStatus}`;
            li.setAttribute('data-followupid', detail.FollowUPID);
            li.setAttribute('data-actiondate', detail.ActionDate);
            li.setAttribute('data-task', detail.Task);
            li.setAttribute('data-remainingdays', detail.RemainingDays);
            li.setAttribute('data-taskupdate', detail.TaskUpdate || '');
            li.setAttribute('data-followupstatus', detail.FollowUpStatus);

           
            li.onclick = function () {
                ViewFollowupDetails(this);
            };
            li.style.cursor = 'pointer';

            
            li.innerHTML = `
                <a href="#" class="check-link">${detail.OrgShortName}</a>
                <span class="m-l-xs">${detail.Task}</span>
            `;

          
            
            document.getElementById('followups').appendChild(li);
            });

        }
        catch{

        }
}

async function RDCompRoom(){
    try{
            const detailResponse = await fetch(`api/RDCompRoom`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();

            const CompRoomListCount = detailData.CompRoom.length;
            $('#CompRoomListCount').text(CompRoomListCount);
            
            
            const $CompRoomListBody = $('#CompRoomListBody');
            $CompRoomListBody.empty();
            
            
            detailData.CompRoom.forEach(detail => {
                const $row = $('<tr>')
                    .attr('onclick', `ViewCompForm(this, ${detail.CompID})`)
                    .css('cursor', 'pointer')
                    .html(`
                        <td style="text-align:left">${detail.Hotel}</td>
                        <td>
                            <b>${detail.GuestName}</b><br>${detail.CompanyName}
                        </td>
                        <td>${detail.PendingSince}</td>
                    `);
                
                $CompRoomListBody.append($row);
            });

        }
        catch{

        }
}


ViewFollowupDetails = function (t) {
    var e = $(t).attr("data-followupid");
    $(".ViewFollowupDetails #ID").val(e), $(".ViewFollowupDetails").modal("show");
    var o = $(t).attr("data-taskupdate");
    $(".ViewFollowupDetails td#TaskUpdate").text(o);
    var n = $(t).attr("data-task");
    $(".ViewFollowupDetails #Task").val(n);
    var l = $(t).attr("data-followupstatus");
    $(".ViewFollowupDetails #FollowUpStatus").val(l);
    var d = $(t).attr("data-actiondate");
    $(".ViewFollowupDetails #ActionDate").val(d);
    var s = $(t).attr("data-remainingdays"),
        r = '<span class="text-green">Completed</span>',
        i = 0,
        p = 1;
    "completed" != l.toLowerCase() && ((p = 0), (i = parseInt(s))),
        0 == p && 0 != i && i > 0 ? (r = "<label>(" + i + ") Day(s) Remaining</label>") : 0 == p && 0 != i && i < 0 && (r = "<label>(" + -1 * i + ") Day(s) Overdue</label>"),
        $(".ViewFollowupDetails td#ActionDate").html(d),
        $(".ViewFollowupDetails td#Status").html(r);
};

DeleteConfirm = function (t) {
    var e = $(".ViewFollowupDetails #ID").val();
    $("#a_delete").attr("href", GRedURL+"/Master/FollowUPDelete?FollowUpID=" + e), $(".ViewFollowupDetails").modal("hide"), $("#DeleteConfimModal").modal("show");
};

async function RDGatepass(){
    try{
        const detailResponse = await fetch(`api/RDGatepass`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const GatePassListCount = detailData.length;
            document.getElementById('GatePassListCount').textContent = GatePassListCount;
            const gatepass_OverdueBody = document.getElementById('gatepass_OverdueBody');


            gatepass_OverdueBody.innerHTML = ''; 

            detailData.forEach(detail => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="text-align:left">${detail.RGPNO} 
                </td>
                <td style="text-align:left"">${detail.ItemName}</td>
                <td style="text-align:left">${detail.Quantity}</td>
                <td style="text-align:left">${detail.Department} 
                </td>
                <td style="text-align:left">${detail.VendorName}</td>
                <td style="text-align:left">${detail.Company}</td>
                <td style="text-align:left">${detail.Out_Date} 
                </td>
                <td style="text-align:left">${detail.ExpReturnDate}</td>
                <td style="text-align:left">${detail.TakenBy}</td>

            `;
            gatepass_OverdueBody.appendChild(row);
            });

        }
        catch{

        }
}

async function RDCapex(){
    try{
        const detailResponse = await fetch(`api/RDCapex`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const capexTotalCount = detailData.length;
            document.getElementById('capexListCount').textContent = capexTotalCount;
            const capexBody = document.getElementById('capexBody');
            capexBody.innerHTML = ''; 
            detailData.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `viewCapex(this, ${detail.ID}, ${detail.A_Q_GM}, ${detail.OrganizationID})`);
            row.style.cursor = 'pointer';
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                        ${detail.Item}<br>

                    </td>
                    <td>${detail.Qty} </td>
                    <td>${detail.Rate}<br><b>${detail.Total}</b> </td>
            `;
            capexBody.appendChild(row);
            });
        }
        catch{

        }
}


  async function viewCapex(t, e, o, n) {
     $(".capexModal .modal-footer").empty();
        var l = "<label onclick=\"CapexActiveShowRej('a','" + e + "','c','" + o + "'," + n + ')" class="btn btn-success">Approve</label>';
        (l += "<label onclick=\"CapexActiveShowRej('r','" + e + "','c','" + o + "'," + n + ')" class="btn btn-danger">Reject</label>'),
            (l += "<label onclick=\"CapexActiveShowRej('h','" + e + "','c','" + o + "'," + n + ')" class="btn btn-warning">Hold</label>'),
            (l += "<label onclick=\"CapexActiveShowRej('rt','" + e + "','c','" + o + "'," + n + ')" class="btn  btn-warning">Return</label>'),
            (l += '<label type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'),
            $(".capexModal .modal-footer").append(l);


    const iframe = document.querySelector('.capexModal iframe');
    iframe.src = `${GRedURL}/capex/home/ViewDetails/`+e;
    $(".capexModal").modal('show');
   
}


function closeModal() {
    const modal = document.querySelector('.capexModal');
    modal.style.display = 'none';
    modal.classList.remove('show');
}

try{
    document.querySelector('.capexModal .close').addEventListener('click', closeModal);
    document.querySelector('.capexModal [data-dismiss="modal"]').addEventListener('click', closeModal);

}catch (error) {
    
  }

  

async function RDLeaveApplication(){
    try{
        const detailResponse = await fetch(`api/RDLeaveApplication`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const leaveListCount = detailData.length;
            document.getElementById('leaveListCount').textContent = leaveListCount;
            const leaveApplicationBody = document.getElementById('leaveApplicationBody');
            leaveApplicationBody.innerHTML = ''; 
            detailData.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `viewLeave(this, ${detail.id},${detail.OrganizationID},"${detail.LeaveType}","${detail.LeaveFrom}", "${detail.LeaveTo}", "${detail.Reason}")`);
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                        ${detail.EmpName}

                    </td>
                    <td>${detail.LeaveFrom} </td>
                    <td>${detail.LeaveTo}</td>
            `;
            leaveApplicationBody.appendChild(row);
            });
        }
        catch{

        }
}

async function RDOpenPosition(){
    try{
        const detailResponse = await fetch(`api/RDOpenPosition`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const OpenPositionsCount = detailData.length;
            document.getElementById('OpenPositionsCount').textContent = OpenPositionsCount;
            const OpenPositionsBody = document.getElementById('OpenPositionsBody');
            OpenPositionsBody.innerHTML = ''; 
            detailData.forEach(detail => {
            const row = document.createElement('tr');
            row.innerHTML = `
                    <td style="text-align:left">${detail.Location} </td>
                    <td>
                        ${detail.Position}

                    </td>
                    <td>${detail.Openedon} </td>
                   
            `;
            OpenPositionsBody.appendChild(row);
            });
        }
        catch{

        }
}

async function RDInterviewAssessment(){
    try{
        const detailResponse = await fetch(`api/RDInterviewAssessment`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const IAListCount = detailData.length;
            document.getElementById('IAListCount').textContent = IAListCount;
            const IAListBody = document.getElementById('IAListBody');
            IAListBody.innerHTML = ''; 
            detailData.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `viewIA(this, ${detail.ID},${detail.OrganizationID})`);
            row.style.cursor = 'pointer';
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                        ${detail.Name}

                    </td>
                    <td>${detail.position} </td>
                   
            `;
            IAListBody.appendChild(row);
            });
        }
        catch{

        }
}

async function RDEmpResignation(){
    try{
        const detailResponse = await fetch(`api/RDEmpResignation`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const ResignListCount = detailData.length;
            document.getElementById('ResignListCount').textContent = ResignListCount;
            const ResignListBody = document.getElementById('ResignListBody');
            ResignListBody.innerHTML = ''; 
            detailData.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `ViewResign(this, ${detail.ID},${detail.OrganizationID})`);
            row.setAttribute('data-name', detail.Name);
            row.setAttribute('data-designation',detail.Designation);
            row.setAttribute('data-department', detail.Department);
            row.setAttribute('data-ResDate', detail.ResDate);
            row.setAttribute('data-emp_code', detail.Emp_Code);
            row.setAttribute('data-DOJ', detail.DOJ);
            row.setAttribute('data-typeofres', detail.TypeofRes);
            row.setAttribute('data-noticeperiod', detail.NoticePeriod);
            row.setAttribute('data-res_reason', detail.Res_Reason);
            row.setAttribute('data-ressubmittedto',detail.Ressubmittedto);
            row.setAttribute('data-lastworkingdays', detail.LastWorkingDays);
            row.setAttribute('data-res_acceptance_date',detail.Res_acceptance_Date);
            row.setAttribute('data-res_acceptance_by', detail.Res_acceptance_By);
            row.style.cursor = 'pointer';

            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                      <strong>  ${detail.Name} </strong><br> ${detail.Designation}

                    </td>
                    <td>${detail.ResDate} </td>
                   
            `;
            ResignListBody.appendChild(row);
            });

        }
        catch{

        }
}

async function RDExitInterview(){
    try{
        const detailResponse = await fetch(`api/RDExitInterview`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const exitInterviewListCount = detailData.length;
            document.getElementById('exitInterviewListCount').textContent = exitInterviewListCount;
            const exitInterviewbody = document.getElementById('exitInterviewBody');
            exitInterviewbody.innerHTML = '';
            detailData.forEach(detail => {
                const row = document.createElement('tr');
                row.setAttribute('onclick', `ViewExitForm(this, ${detail.Exitid},${detail.OrganizationID})`);
                row.style.cursor = 'pointer';
                row.innerHTML = `
                    <td style="text-align:left"">${detail.Hotel}</td>
                    <td style="text-align:center"><strong>${detail.EmpName}</strong> <br> ${detail.Position}
                    </td>
                    <td style="text-align:left">${detail.FinalComment} 
                    </td>
    
                `;
                exitInterviewbody.appendChild(row);
               
            });
        }
        catch{

        }
};







async function MainingGuideChart(chartType) {
    // showLoader(chartType);
    
    try {
        const level = document.getElementById('level').value || '';
        const response = await fetch(`api/CEO_ManningGuide/?level=${level}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const detailData = await response.json();
        const toprequestbody = document.getElementById('mannningguide_body');
        toprequestbody.innerHTML = ''; 

        detailData.forEach((item, index)=> {
        
        const row = document.createElement('tr');
        row.setAttribute('onclick', `MainingGuideDetails('${level}' ,${item.OrganizationID})`);
        row.style.cursor = 'pointer';
        row.innerHTML = `
                <td class="text-center">${index + 1}</td>
                <td>${item.HTL}</td>
                <td class="text-center">${formatToINR(item.Budget)}</td>
                <td class="text-center">${formatToINR(item.Actual)}</td>
                <td class="text-center" style="color: ${item.Variance < 0 ? 'green' : 'red'};">
                    ${formatToINR(item.Variance)}
                </td>
                <td class="text-center">${formatToINR(item.HC_Budget)}</td>
                <td class="text-center">${formatToINR(item.HC_Actual)}</td>
                <td class="text-center" style="color: ${item.HC_Variance < 0 ? 'green' : 'red'};">
                    ${formatToINR(item.HC_Variance)}
                </td>
            
        `;
            toprequestbody.appendChild(row);
            });

            hideLoader(chartType);


            } 
    catch (error) {
        hideLoader(chartType);
        console.error('Error fetching mainingGuideChart data:', error);
    }
}

async function MainingGuideDetails(level,OrganizationID){
    let myModal = new bootstrap.Modal(document.getElementById('manningguideModal'));
            myModal.show();
            showLoader('manningDetailsLoader');

    
            try {
                const response = await fetch(`api/CEO_ManningGuideDetails/?level=${level}&OrganizationID=${OrganizationID}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                
                const data = await response.json();
                hideLoader('manningDetailsLoader');
                
                
                drawOnRollChart(data.OnRoll);
                drawContractChart(data.Contract);
                drawSharedServicesChart(data.SharedServices);
                drawCafeteriaChart(data.CafeteriaMealCost);
                drawEmployeeInsuranceChart(data.EmployeeInsuranceCost);

                } 
            catch (error) {
                hideLoader('manningDetailsLoader');

                console.error('Error fetching mainingGuideChart data:', error);
            }
}

function drawOnRollChart(data) {
    const onRollChartDom = document.getElementById('onrollChart');
    const onRollChart = echarts.init(onRollChartDom);
    
    const HTL = data.map(item => item.Department);
    const Budget = data.map(item => item.Budget);
    const Actual = data.map(item => item.Actual);
    const Variance = data.map(item => item.Variance);

    const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { data: ['Budget', 'Actual', 'Variance'] },
        grid: { left: '3%', right: '3%', bottom: '10%', containLabel: true },
        xAxis: {
            type: 'category',
            data: HTL,
            axisLabel: { interval: 0, rotate: 30, fontSize: 9 },
            barCategoryGap: '50%',
        },
        yAxis: { type: 'value' },
        series: [
            {
                name: 'Budget',
                type: 'bar',
                barWidth: '30%',
                data: Budget,
                itemStyle: { color: '#FF902F' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Actual',
                type: 'bar',
                barWidth: '30%',
                data: Actual,
                itemStyle: { color: 'rgb(140,217,201)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                },}
            },
            {
                name: 'Variance',
                type: 'bar',
                barWidth: '30%',
                data: Variance,
                itemStyle: { color: 'rgb(238,164,127)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    let absValue = Math.abs(value);  
                    let formattedValue;
                    if (absValue >= 10000000) {
                        formattedValue = (absValue / 10000000).toFixed(0) + 'Cr'; 
                    } else if (absValue >= 100000) {
                        formattedValue = (absValue / 100000).toFixed(0) + 'L';  
                    } else if (absValue >= 1000) {
                        formattedValue = (absValue / 1000).toFixed(0) + 'k';    
                    } else {
                        formattedValue = absValue;  
                    }
                    return value < 0 ? '-' + formattedValue : formattedValue;
                                       
                } }
            }
        ]
    };

    onRollChart.setOption(option);
}

function drawContractChart(data) {
    const contractChartDom = document.getElementById('ContractChart');
    const contractChart = echarts.init(contractChartDom);

    const HTL = data.map(item => item.Department);
    const Budget = data.map(item => item.Budget);
    const Actual = data.map(item => item.Actual);
    const Variance = data.map(item => item.Variance);

    const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { data: ['Budget', 'Actual', 'Variance'] },
        grid: { left: '3%', right: '3%', bottom: '10%', containLabel: true },
        xAxis: {
            type: 'category',
            data: HTL,
            axisLabel: { interval: 0, rotate: 30, fontSize: 9 },
            barCategoryGap: '50%',
        },
        yAxis: { type: 'value' },
        series: [
            {
                name: 'Budget',
                type: 'bar',
                barWidth: '30%',
                data: Budget,
                itemStyle: { color: '#FF902F' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Actual',
                type: 'bar',
                barWidth: '30%',
                data: Actual,
                itemStyle: { color: 'rgb(140,217,201)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Variance',
                type: 'bar',
                barWidth: '30%',
                data: Variance,
                itemStyle: { color: 'rgb(238,164,127)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    let absValue = Math.abs(value);  
                    let formattedValue;
                    if (absValue >= 10000000) {
                        formattedValue = (absValue / 10000000).toFixed(0) + 'Cr'; 
                    } else if (absValue >= 100000) {
                        formattedValue = (absValue / 100000).toFixed(0) + 'L';  
                    } else if (absValue >= 1000) {
                        formattedValue = (absValue / 1000).toFixed(0) + 'k';    
                    } else {
                        formattedValue = absValue;  
                    }
                    return value < 0 ? '-' + formattedValue : formattedValue;
                                       
                } }
            }
        ]
    };

    contractChart.setOption(option);
}

function drawSharedServicesChart(data) {
    const sharedServicesChartDom = document.getElementById('SharedServicesChart');
    const sharedServicesChart = echarts.init(sharedServicesChartDom);

    const HTL = data.map(item => item.Department);
    const Budget = data.map(item => item.Budget);
    const Actual = data.map(item => item.Actual);
    const Variance = data.map(item => item.Variance);

    const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { data: ['Budget', 'Actual', 'Variance'] },
        grid: { left: '3%', right: '3%', bottom: '10%', containLabel: true },
        xAxis: {
            type: 'category',
            data: HTL,
            axisLabel: { interval: 0, rotate: 30, fontSize: 9 },
            barCategoryGap: '50%',
        },
        yAxis: { type: 'value' },
        series: [
            {
                name: 'Budget',
                type: 'bar',
                barWidth: '30%',
                data: Budget,
                itemStyle: { color: '#FF902F' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Actual',
                type: 'bar',
                barWidth: '30%',
                data: Actual,
                itemStyle: { color: 'rgb(140,217,201)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Variance',
                type: 'bar',
                barWidth: '30%',
                data: Variance,
                itemStyle: { color: 'rgb(238,164,127)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    let absValue = Math.abs(value);  
                    let formattedValue;
                    if (absValue >= 10000000) {
                        formattedValue = (absValue / 10000000).toFixed(0) + 'Cr'; 
                    } else if (absValue >= 100000) {
                        formattedValue = (absValue / 100000).toFixed(0) + 'L';  
                    } else if (absValue >= 1000) {
                        formattedValue = (absValue / 1000).toFixed(0) + 'k';    
                    } else {
                        formattedValue = absValue;  
                    }
                    return value < 0 ? '-' + formattedValue : formattedValue;
                                       
                } }
            }
        ]
    };

    sharedServicesChart.setOption(option);
}

function drawCafeteriaChart(data) {
    const cafeteriaChartDom = document.getElementById('cafteriaChart');
    const cafeteriaChart = echarts.init(cafeteriaChartDom);

    const HTL = data.map(item => item.Department);
    const Budget = data.map(item => item.Budget);
    const Actual = data.map(item => item.Actual);
    const Variance = data.map(item => item.Variance);

    const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { data: ['Budget', 'Actual', 'Variance'] },
        grid: { left: '3%', right: '3%', bottom: '10%', containLabel: true },
        xAxis: {
            type: 'category',
            data: HTL,
            axisLabel: { interval: 0, fontSize: 9 },
            barCategoryGap: '50%',
        },
        yAxis: { type: 'value' },
        series: [
            {
                name: 'Budget',
                type: 'bar',
                barWidth: '30%',
                data: Budget,
                itemStyle: { color: '#FF902F' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Actual',
                type: 'bar',
                barWidth: '30%',
                data: Actual,
                itemStyle: { color: 'rgb(140,217,201)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Variance',
                type: 'bar',
                barWidth: '30%',
                data: Variance,
                itemStyle: { color: 'rgb(238,164,127)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    let absValue = Math.abs(value);  
                    let formattedValue;
                    if (absValue >= 10000000) {
                        formattedValue = (absValue / 10000000).toFixed(0) + 'Cr'; 
                    } else if (absValue >= 100000) {
                        formattedValue = (absValue / 100000).toFixed(0) + 'L';  
                    } else if (absValue >= 1000) {
                        formattedValue = (absValue / 1000).toFixed(0) + 'k';    
                    } else {
                        formattedValue = absValue;  
                    }
                    return value < 0 ? '-' + formattedValue : formattedValue;
                                       
                } }
            }
        ]
    };

    cafeteriaChart.setOption(option);
}

function drawEmployeeInsuranceChart(data) {
    const employeeChartDom = document.getElementById('employeeChart');
    const employeeChart = echarts.init(employeeChartDom);

    const HTL = data.map(item => item.Department);
    const Budget = data.map(item => item.Budget);
    const Actual = data.map(item => item.Actual);
    const Variance = data.map(item => item.Variance);

    const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { data: ['Budget', 'Actual', 'Variance'] },
        grid: { left: '3%', right: '3%', bottom: '10%', containLabel: true },
        xAxis: {
            type: 'category',
            data: HTL,
            axisLabel: { interval: 0,fontSize: 9 },
            barCategoryGap: '50%',
        },
        yAxis: { type: 'value' },
        series: [
            {
                name: 'Budget',
                type: 'bar',
                barWidth: '30%',
                data: Budget,
                itemStyle: { color: '#FF902F' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Actual',
                type: 'bar',
                barWidth: '30%',
                data: Actual,
                itemStyle: { color: 'rgb(140,217,201)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    if (value >= 10000000) {
                        return (value / 10000000).toFixed(0) + 'Cr'; 
                    } else if (value >= 100000) {
                        return (value / 100000).toFixed(0) + 'L';  // Lakhs (for values >= 1 lakh)
                    } else if (value >= 1000) {
                        return (value / 1000).toFixed(0) + 'k';    // Thousands (for values >= 1 thousand)
                    } else {
                        return value;  // If value is below 1000, show it as it is
                    }
                }, }
            },
            {
                name: 'Variance',
                type: 'bar',
                barWidth: '30%',
                data: Variance,
                itemStyle: { color: 'rgb(238,164,127)' },
                label: { show: true, position: 'top', formatter: function (params) {
                    let value = params.value;
                    let absValue = Math.abs(value);  
                    let formattedValue;
                    if (absValue >= 10000000) {
                        formattedValue = (absValue / 10000000).toFixed(0) + 'Cr'; 
                    } else if (absValue >= 100000) {
                        formattedValue = (absValue / 100000).toFixed(0) + 'L';  
                    } else if (absValue >= 1000) {
                        formattedValue = (absValue / 1000).toFixed(0) + 'k';    
                    } else {
                        formattedValue = absValue;  
                    }
                    return value < 0 ? '-' + formattedValue : formattedValue;
                                       
                } }
            }
        ]
    };

    employeeChart.setOption(option);
}

function valueFormatter(params) {
    return formatToINR(params.value);
}

function varianceFormatter(params) {
    const value = params.value;
    const absValue = Math.abs(value);
    const formattedValue = formatToINR(absValue);
    return value < 0 ? '-' + formattedValue : formattedValue;
}

function formatToINR(number) {
    if (number === undefined || number === null || isNaN(number)) {
        return 0;
    }
    return number.toLocaleString('en-IN');
}


try {
document.getElementById('revenueHeading').addEventListener('click', async function () {
    let myModal = new bootstrap.Modal(document.getElementById('revenueModal'));
    myModal.show();
    const chartType='revnueDetailsLoader';
    showLoader(chartType);


    timeRangeText = document.getElementById('total-revenue-label').innerText

    let RT = 1;
    switch (timeRangeText) {
        case 'Yesterday':
            RT = 1;
            break;
        case 'Weekly':
            RT = 2;
            break;
        case 'Monthly':
            RT = 3;
            break;
        case 'Yearly':
            RT = 4;
            break;
    }

    const Type = 'Total Revenue'

    const chartDom = document.getElementById('totalRevenuemodelChart');
    const revenueModalChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEORevenueGridDetailsModalData?RT=${RT}&Type=${Type}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        

        const data = await response.json();
        const axis_data = data.Table.map(item => item.Hotel);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);


        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total Revenue']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total Revenue',
                    type: 'bar',
                    barWidth: '40%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            let value = params.value;
                            if (value >= 10000000) {
                                return (value / 10000000).toFixed(1) + 'Cr'; 
                            } else if (value >= 100000) {
                                return (value / 100000).toFixed(1) + 'L';  
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'k';   
                            } else {
                                return value; 
                            }
                        }
                    }
                },
            ]
        };


        revenueModalChart.setOption(option);
        hideLoader(chartType);
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }


});
}
catch(error){
    

}


try {
document.getElementById('RoomRevenueHeading').addEventListener('click', async function () {
    let myModal = new bootstrap.Modal(document.getElementById('revenueModal'));
    myModal.show();

    timeRangeText = document.getElementById('total-revenue-label').innerText

    let RT = 1;
    switch (timeRangeText) {
        case 'Yesterday':
            RT = 1;
            break;
        case 'Weekly':
            RT = 2;
            break;
        case 'Monthly':
            RT = 3;
            break;
        case 'Yearly':
            RT = 4;
            break;
    }

    const Type = 'Room Revenue'

    const chartDom = document.getElementById('totalRevenuemodelChart');
    const revenueModalChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEORevenueGridDetailsModalData?RT=${RT}&Type=${Type}`);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        const axis_data = data.Table.map(item => item.Hotel);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);


        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Room Revenue']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Room Revenue',
                    type: 'bar',
                    barWidth: '40%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            let value = params.value;
                            if (value >= 10000000) {
                                return (value / 10000000).toFixed(1) + 'Cr'; // Crores (for values >= 1 crore)
                            } else if (value >= 100000) {
                                return (value / 100000).toFixed(1) + 'L';  // Lakhs (for values >= 1 lakh)
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'k';    // Thousands (for values >= 1 thousand)
                            } else {
                                return value;  // If value is below 1000, show it as it is
                            }
                        }
                    }
                },
            ]
        };


        revenueModalChart.setOption(option);
    } catch (error) {
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }


});
}
catch(error){
   

}



try {
document.getElementById('FBRevenueHeading').addEventListener('click', async function () {
    let myModal = new bootstrap.Modal(document.getElementById('revenueModal'));
    myModal.show();

    timeRangeText = document.getElementById('total-revenue-label').innerText

    let RT = 1;
    switch (timeRangeText) {
        case 'Yesterday':
            RT = 1;
            break;
        case 'Weekly':
            RT = 2;
            break;
        case 'Monthly':
            RT = 3;
            break;
        case 'Yearly':
            RT = 4;
            break;
    }

    const Type = 'FB Revenue'

    const chartDom = document.getElementById('totalRevenuemodelChart');
    const revenueModalChart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/CEORevenueGridDetailsModalData?RT=${RT}&Type=${Type}`);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        const axis_data = data.Table.map(item => item.Hotel);
        const Total = data.Table.map(item => item.Total === 0 ? null : item.Total);


        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['FB Revenue']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'FB Revenue',
                    type: 'bar',
                    barWidth: '40%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                        formatter: function (params) {
                            let value = params.value;
                            if (value >= 10000000) {
                                return (value / 10000000).toFixed(1) + 'Cr'; // Crores (for values >= 1 crore)
                            } else if (value >= 100000) {
                                return (value / 100000).toFixed(1) + 'L';  // Lakhs (for values >= 1 lakh)
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'k';    // Thousands (for values >= 1 thousand)
                            } else {
                                return value;  // If value is below 1000, show it as it is
                            }
                        }
                    }
                },
            ]
        };


        revenueModalChart.setOption(option);
    } catch (error) {
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }


});
}
catch(error){
   

}


async function RDPADPList(){
    try{
        const detailResponse = await fetch(`api/RDPADPList`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const PADPListCount = detailData.length;
            document.getElementById('PADPListCount').textContent = PADPListCount;
            const PADPListBody = document.getElementById('PADPListBody');
            PADPListBody.innerHTML = ''; 
            detailData.forEach(detail => {
            const row = document.createElement('tr');
            row.setAttribute('onclick', `viewPADP(this, ${detail.ID},${detail.UserID},${detail.OrganizationID},"${detail.RT}")`);
            row.innerHTML = `
                    <td style="text-align:left">${detail.Hotel} </td>
                    <td>
                       ${detail.EmployeeName} <br>

                    </td>
                    <td>
                    ${detail.SalaryIncrementOption.includes('%') 
                        ? `<span> ${detail.SalaryIncrementOption}</span>`
                        : `<span><b><u>Salary Correction</u></b></span>
                    <br>
                    <span><b style="display: inline-block;min-width:50px">From:</b>${detail.SalaryCorrectionFrom}</span>
                    <span> / <b style="display: inline-block;min-width:50px">To:</b>${detail.SalaryCorrection}</span>`}
                    
                    
                    
                     </td>
                   
            `;
            PADPListBody.appendChild(row);
          
               
            });
        }
        catch{

        }
}






function downloadChart(chartId) {
    const chartElement = document.getElementById(chartId); 
    html2canvas(chartElement, { scale: 2 }).then((canvas) => { 
        const imgData = canvas.toDataURL('image/png');

        
        const { jsPDF } = window.jspdf;

       
        const imgWidth = canvas.width;
        const imgHeight = canvas.height;
        

        const pdfWidth = 595.28; // A4 width
        const pdfHeight = 841.89; 

        
        const widthRatio = pdfWidth / imgWidth;
        const heightRatio = pdfHeight / imgHeight;
        const ratio = Math.min(widthRatio, heightRatio);

        const scaledWidth = imgWidth * ratio;
        const scaledHeight = imgHeight * ratio;

      
         const pdf = new jsPDF('l', 'pt', [pdfWidth, scaledHeight]);

       
        pdf.addImage(imgData, 'PNG', 0, 0, scaledWidth, scaledHeight);
        pdf.save(`${chartId}.pdf`);
    });
}



function downloadChartnew() {
    const content = document.getElementById('HotelRevenue'); // Selects the content to download

    const options = {
        margin: 0.5,
        filename: 'VisitDetails.pdf',
        image: { type: 'jpeg', quality: 1 },
        html2canvas: { scale: 2, scrollX: 0, scrollY: 0, useCORS: true },
        jsPDF: { unit: 'in', format: 'A4', orientation: 'portrait' }
    };

    
    html2pdf().from(content).set(options).save();
}


function downloadChartnew1() {
    $('#dsrDetails').modal('show');
    
    setTimeout(() => {
        const pdfArea = document.getElementById('pdfCaptureArea');
        
        const options = {
            margin: 0.5,
            filename: 'VisitDetails.pdf',
            image: { type: 'jpeg', quality: 1 },
            html2canvas: { scale: 2, useCORS: true, scrollY: 0, scrollX: 0 },
            jsPDF: { unit: 'in', format: 'A4', orientation: 'portrait' }
        };

        html2pdf().from(pdfArea).set(options).save();
    }, 500); // Wait for the content to render
}

AddFollowTask = function () {
    
    var t = $("[name='I']").val();
    $("#FollowTaskModel [name='Responsibility']").empty(),
        $("#FollowTaskModel [name='ResponsibilityUserID']").val(""),
        $("#FollowTaskModel [name='ro']").val($("[name='I'].srI").val()),
        $("#FollowTaskModel [name='Responsibility']").removeAttr("readonly"),
        $("#FollowTaskModel [name='I']").val(t),
        $("#FollowTaskModel [name='FollowUpDate']").val(""),
        $("#FollowTaskModel [name='ActionDate']").val(""),
        $("#FollowTaskModel [name='Task']").val(""),
        $("#FollowTaskModel [name='Header']").val(""),
        $("#FollowTaskModel [name='priority']").val(""),
        $("#FollowTaskModel [name='TaskUpdate']").val(""),
        $("#FollowTaskModel [name='Status']").val("Pending"),
        $("#FollowTaskModel [name='FollowUpID']").val(0),
        $(".datepicker").datepicker({ format: "dd-MM-yy" }),
        $("#FollowTaskModel").modal("show"),
        BindUserAutoComplete();
}

async function BindUserAutoComplete  () {
    var t = $("#FollowTaskModel [name='I']").find("option:selected").val();
    try {
        
        const response = await fetch(`api/UserList?O=${t}`);
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        if (data) {
            // Clear the Responsibility dropdown and reset values
            const responsibilityDropdown = document.querySelector("#FollowTaskModel [name='Responsibility']");
            responsibilityDropdown.innerHTML = "<option value='' data-ResponsibilityID='0' data-usertype='0'>Select</option>";

            // Populate the Responsibility dropdown with the data
            data.forEach((e) => {
                const option = document.createElement("option");
                option.value = e.UserID;
                option.setAttribute("data-ResponsibilityID", e.UserID);
                option.setAttribute("data-usertype", e.UserType);
                option.textContent = `${e.Name} - ${e.UserType}-${e.Department}`;

                if (e.UserType === "GM") {
                    option.selected = true;
                }

                responsibilityDropdown.appendChild(option);
            });

            
            const selectedOption = responsibilityDropdown.querySelector("option:checked");
            document.querySelector("#FollowTaskModel [name='ResponsibilityUserID']").value = selectedOption ? selectedOption.getAttribute("data-ResponsibilityID") : "";
        }
    } catch (error) {
        console.error('Error fetching user list:', error);
    }
}
async function organizattionlist() {
    
    try {
        const selectOrganazation = document.getElementById('org_follow');
        const detailResponse = await fetch(`api/CEOORGList/`);
        if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
        const detailData = await detailResponse.json();
        selectOrganazation.innerHTML = '';

        detailData.Table.forEach((org, index) => {
            const option = document.createElement('option');
            option.value = org.OrganizationID; 
            option.textContent = org.Organization_name; 

            
            if (index === 0) {
                option.selected = true;
                
            }

            selectOrganazation.appendChild(option);
        });
    
    } catch (error) {
        console.error('Error fetching topSrmsDetailsModal data:', error);
        document.getElementById('topSrmsCompletedDurationDetailsModalBody').innerText = 'Error fetching details.';
    }
}
organizattionlist();

function formatDate() {
    var input = document.getElementById("actiondate");
    var dateValue = input.value;

    if (dateValue) {
      // Parse the date in yyyy-mm-dd format
      var date = new Date(dateValue);
      
      // Get day, month, and year
      var day = ("0" + date.getDate()).slice(-2);
      var month = date.toLocaleString('default', { month: 'long' });
      var year = date.getFullYear().toString().slice(-2);
      
      // Set the formatted date
      input.value = `${day}-${month}-${year}`;
    }
  }

  async function DiscardsChartData(button,chartType, rangeType) {
    updateButtonState(button);
    showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('discardplot');
    const discardplotchart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/discardsChartData/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.map(item => item.Hotel);
        const OrganizationID = data.map(item => item.OrganizationID);
        const Total = data.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };
        discardplotchart.setOption(option);
        discardplotchart.RT = RT;
        discardplotchart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#DiscardsDetailsModal').modal('show');
                showLoader('discardLoader');
                const RT = discardplotchart.RT;
                const detailResponse = await fetch(`api/DiscardsDetailsChartData/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('DiscardsDetailsModalBody');
                toprequestbody.innerHTML = ''; 
                
                detailData.forEach((detail, index) => {
                    const itemDetails = JSON.parse(detail.ItemDetails);
                    let rowTotalQty = 0;
                    let rowTotalCost = 0;

                    itemDetails.forEach(item => {
                        rowTotalQty += item.TotalQty || 0;
                        rowTotalCost += item.TotalCost || 0;
                    });
                    const rowTotalRate = (rowTotalCost / rowTotalQty).toFixed(0)

                
                    
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td style="text-align:center">${index + 1 } 
                            </td>
                        <td style="text-align:left">${detail.HTL} 
                            </td>
                            <td style="text-align:left"">${detail.DiscardDate}</td>
                            <td style="text-align:left">${detail.Category}</td>
                            <td style="text-align:left">${detail.GMStatus} 
                            </td>
                            <td style="text-align:left">${rowTotalQty.toFixed(0)}</td>
                            <td style="text-align:left">${rowTotalRate}</td>
                            <td style="text-align:left">${rowTotalCost.toFixed(0)} 
                            </td>
                            <td style="text-align:center;color:blue" data-item-details='${JSON.stringify(detail.ItemDetails)}'  onclick="discardDetails(this)">
                            <span >
                        <i class="fa fa-eye" aria-hidden="true"></i>
                    </span>
                    </td> 
            
                    `;
                    toprequestbody.appendChild(row);
                    });
                    hideLoader('discardLoader'); 
               
                
            } catch (error) {
                hideLoader('discardLoader') 
                console.error('Error fetching ChecklistDetailsmodal data:', error);
                document.getElementById('ChecklistDetailsmodalbody').innerText = 'Error fetching details.';
            }
                    
            });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching discardsChartData  data:', error);
    }


}


function discardDetails(element) {
    let itemDetails = element.getAttribute('data-item-details');

    try {
        if (typeof itemDetails === 'string') {
            itemDetails = JSON.parse(itemDetails);
        }

        const parsedItemDetails = Array.isArray(itemDetails) ? itemDetails : JSON.parse(itemDetails);

        
        if (!Array.isArray(parsedItemDetails)) {
            console.error("Parsed ItemDetails is not an array:", parsedItemDetails);
            return;
        }

       
        const itemDetailsBody = document.getElementById('ItemDetailsModalBody');
        itemDetailsBody.innerHTML = ''; 
        
        parsedItemDetails.forEach((item, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${item.Item}</td>
                <td>${item.MonthLess6 || '-'}</td>
                <td>${item.Month6to9 || '-'}</td>
                <td>${item.Month9to15 || '-'}</td>
                <td>${item.MonthMore15 || '-'}</td>
                <td>${item.TotalQty}</td>
                <td>${item.Rate}</td>
                <td>${item.TotalCost}</td>
                <td>${item.Remarks || '-'}</td>
            `;
            itemDetailsBody.appendChild(row);
        });

        
        $('#ItemDetailsModal').modal('show');
    } catch (error) {
        console.error("Error parsing itemDetails:", error);
    }
}


async function LostAndFoundChart(button,chartType, rangeType) {
    updateButtonState(button);
    // showLoader(chartType);
    const RT = rangeType;
    const chartDom = document.getElementById('lfChart');
    const lfplotchart = echarts.init(chartDom);
    try {
        const response = await fetch(`api/LostAndFoundChart/?RT=${RT}`);
        if (!response.ok) {
            hideLoader(chartType);
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        hideLoader(chartType);
        const axis_data = data.map(item => item.Hotel);
        const OrganizationID = data.map(item => item.OrganizationID);
        const Total = data.map(item => item.Total === 0 ? null : item.Total);

        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '3%', right: '3%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: axis_data,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 10
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '25%',
                    data: Total,
                    itemStyle: { color: '#FF902F' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };
        lfplotchart.setOption(option);
        lfplotchart.RT = RT;

        lfplotchart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
                $('#lfModalDetails').modal('show');
                showLoader('lfLoader');
                const RT = lfplotchart.RT;
                const detailResponse = await fetch(`api/LostAndFoundChartDataDetails/?OrganizationID=${orgId}&RT=${RT}`);
                if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);
                const detailData = await detailResponse.json();
                const toprequestbody = document.getElementById('lfModalDetailsbody');
                toprequestbody.innerHTML = ''; 
                
                detailData.forEach((detail, index) => {

                    let statusContent =  `<strong>${detail.Status}</strong>`; 

                    if (detail.Status === "Handed over to Guest") {
                        statusContent += `,<br><strong> Name:</strong> ${detail.HandedOvertoGuest},<br><strong> On: </strong>${detail.Status_HandedGuestOn}`;
                    } else if (detail.Status === "Handed over to Employee") {
                        statusContent += `,<br><strong> Name:</strong>${detail.HandedOverEmpName},<br><strong> On: </strong> ${detail.Status_HandedEmployeeOn}`;
                    }

                    
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td style="text-align:center">${index + 1 } 
                            </td>
                        <td style="text-align:left">${detail.HTL} 
                            </td>
                            <td style="text-align:left"">${detail.Datefoundon}</td>
                            <td style="text-align:left">${detail.RoomNumber}</td>
                            <td style="text-align:left">${detail.GuestName} 
                            </td>
                            <td style="text-align:left">${detail.ItemType}</td>
                             <td style="text-align:left">${statusContent}</td>

                            
                            
                            
                           
                             
                    `;
                    toprequestbody.appendChild(row);
                    });
                    hideLoader('lfLoader'); 
               
                
            } catch (error) {
                hideLoader('lfLoader') 
                console.error('Error fetching LostAndFoundChartDataDetails data:', error);
                document.getElementById('lfModalDetailsbody').innerText = 'Error fetching details.';
            }
                    
            });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching discardsChartData  data:', error);
    }


}
