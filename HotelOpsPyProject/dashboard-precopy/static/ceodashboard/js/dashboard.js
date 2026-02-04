
let selectedTimeRange = null;

function showLoader(chartType) {
    document.getElementById(`loader-${chartType}`).style.display = 'flex';
}


function hideLoader(chartType) {
    document.getElementById(`loader-${chartType}`).style.display = 'none';
}

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

async function ShowGlitchDetails(){
    try {
        const RT = selectedTimeRange

        const response = await fetch(`api/GlitchDetails/?RT=${RT}`);
        if (!response.ok) {
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

        data.GlitchData.forEach(item => {
            const row = `
                <tr data-status="${item.Status}">
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
        document.getElementById('GlitchDetailsModal').style.display = 'block';
    } catch (error) {
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

async function ShowCompRoomDetails() {
    try {
        const RT = selectedTimeRange
        const response = await fetch(`api/CompRoomDetails/?RT=${RT}`);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        const tableBody = document.getElementById('compRoomDetailsBody');
        tableBody.innerHTML = '';

        data.CompRoomData.forEach(item => {
            const row = `
                <tr>
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


        document.getElementById('CompRoomDetailsModal').style.display = 'block';



    } catch (error) {
        console.error('Error fetching CompRoomDetails data:', error);
    }
}


async function ShowIncidentDetails(){
    try {
        const RT = selectedTimeRange

        const response = await fetch(`api/IncidentDetails/?RT=${RT}`);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }


        const data = await response.json();
        const tableBody = document.getElementById('IncidentDetailsBody');
        tableBody.innerHTML = '';
        

        data.IncidentData.forEach(item => {
                        const row = `
            <tr>
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


        document.getElementById('IncidentDetailsModal').style.display = 'block';
    } 
    catch (error) {
        console.error('Error fetching IncidentDetails data:', error);
    }
}

async function ShowTotalEquipment() {
    try {
        const RT = selectedTimeRange

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
        $('#EnqEQDetailsModal').modal('show');
    } catch (error) {
    console.error('Error fetching EnqEQDetailsModal data:', error);
    document.getElementById('EnqEQDetailsModalBody').innerText = 'Error fetching details.';
    }
}

async function ShowTotalUWEquipment() {
try {
    const RT = selectedTimeRange
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
                    
    $('#EnqEQDetailsModal').modal('show');
    
} 
catch (error) {
        console.error('Error fetching EnqEQDetailsModal data:', error);
        document.getElementById('EnqEQDetailsModalBody').innerText = 'Error fetching details.';
 }
}

async function ShowTotalUAEquipment() {
    try {
        const RT = selectedTimeRange
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
  
        $('#EnqEQDetailsModal').modal('show');
    
    } 
    catch (error) {
        console.error('Error fetching EnqEQDetailsModal data:', error);
        document.getElementById('EnqEQDetailsModalBody').innerText = 'Error fetching details.';
    }
}

async function ShowTotalBreakdown(){
    try {
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

                    
        $('#EnqEQBreakdownDetailsModal').modal('show');
                
    } 
    catch (error) {
        console.error('Error fetching EnqEQBreakdownDetailsModal data:', error);
        document.getElementById('EnqEQBreakdownDetailsModalbody').innerText = 'Error fetching details.';
    }
}


async function ShowTotalMaintenance(){
    try {
        const RT = selectedTimeRange
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

                            
        $('#EnqEQMaintanceDetailsModal').modal('show');       
    } 
    catch (error) {
            console.error('Error fetching EnqEQMaintanceDetailsModal data:', error);
            document.getElementById('EnqEQMaintanceDetailsModalbody').innerText = 'Error fetching details.';
    }
}


async function ShowTotalPendingMaintenance(){
    try {
        const RT = selectedTimeRange
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

        $('#EnqEQMaintanceDetailsModal').modal('show');
            
        } 
    catch (error) {
            console.error('Error fetching EnqEQMaintanceDetailsModal data:', error);
            document.getElementById('EnqEQMaintanceDetailsModalbody').innerText = 'Error fetching details.';
    }
}

function closeModal() {
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
    console.log("in js code ");
    switch (pageId) {
        case 'CeoDashboard':
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData(firstButton, 1);
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
            warningLettersDatachart(firstButton,'warnletter', 1);
            cateringSaleDatachart(firstButton,'catering', 1);
            dailyBreakageDataChart(firstButton,'breakreport', 1);
            restaurantFeedbackDataChart(firstButton,'feedback', 1);
            organizationList()
    
            break;
        case 'RoomDivisionDashboard':
            HotelRevenueDataChart1(firstButton,'htlissue', 1);
            payMasterDatachart(firstButton,'paymaster', 1);
            out_of_orderChart(firstButton,'outoforder', 1);
            total_SRMSRequestChart(firstButton,'srms', 1);
            RDGuestMetChart(firstButton,'GMguest', 1);
            PpmRoomsDatachart(firstButton,'PPM', 1);
            TopSRMSrequestChart(firstButton,'topSRMS', 1);
            total_SRMSRequestCompletionChart(firstButton,'totalSRMS', 1);
            trainingHoursDatachart(firstButton,'training', 1);
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
            organizationList()
            break;

        case 'FBServiceDashboard':
            console.log("in FB sevice dashbaord")
            HotelRevenueDataChart1(firstButton,'htlissue', 1);
            total_SRMSRequestChart(firstButton,'srms', 1);
            RDGuestMetChart(firstButton,'GMguest', 1);
            TopSRMSrequestChart(firstButton,'topSRMS', 1);
            total_SRMSRequestCompletionChart(firstButton,'totalSRMS', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            break;
    

        case 'salesDashboard':
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData(firstButton, 1);
            CEORevenueTotalData(firstButton,'CEOData', 1);
            SalesContractChartData(firstButton,'sc', 1);
            DSRChart(firstButton,'dsr',1);
            out_of_orderChart(firstButton,'outoforder', 1);
            RDGuestMetChart(firstButton,'GMguest', 1);
            ArCollectionDatachart(firstButton,'arc', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            forecastDatachart(firstButton, 'occ',1);
            forecastAdrDatachart(firstButton,'adr', 1);
            break;
        case 'marketingDashboard':
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData(firstButton, 1);
            CEORevenueTotalData(firstButton,'CEOData', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            break;
        case 'revenueDashboard':
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData(firstButton, 1);
            CEORevenueTotalData(firstButton,'CEOData', 1);
            SalesContractChartData(firstButton,'sc', 1);
            out_of_orderChart(firstButton,'outoforder', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            forecastDatachart(firstButton, 'occ',1);
            forecastAdrDatachart(firstButton,'adr', 1);
            break;
        case 'financeDashboard':
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData(firstButton, 1);
            CEORevenueTotalData(firstButton,'CEOData', 1);
            SalesContractChartData(firstButton,'sc', 1);
            out_of_orderChart(firstButton,'outoforder', 1);
            ArCollectionDatachart(firstButton,'arc', 1);
            trainingHoursDatachart(firstButton,'training', 1);
            forecastDatachart(firstButton, 'occ',1);
            forecastAdrDatachart(firstButton,'adr', 1);
            payMasterDatachart(firstButton,'paymaster', 1);
            organizationList()
            break;
        case 'D_OpsDashboard':
            HotelRevenueDataChart(firstButton,'hotelrevenue', 1);
            HotelRevenueData(firstButton, 1);
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
            maintanceBreakdown(firstButton,'maintance', 1);
            organizationList();
        case 'HRDashboard':
            HotelRevenueDataChart1(firstButton,'htlissue', 1);
            trainingHoursDatachart(firstButton,'training', 1);
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

async function HotelRevenueData(button,rangeType){
try {
    selectedTimeRange = rangeType;
    updateButtonState(button);
    const RT = selectedTimeRange

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
        const Title = data.Table.map(item => item.Title);
        const YOD = data.Table.map(item => item.YOD);
        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' }
            },
            legend: {
                data: ['Total']
            },
            grid: {
                left: '5%', right: '5%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: Title,
                axisLabel: {
                    interval: 0,
                    rotate: 45,  // Tilts labels for readability
                    fontSize: 9,
                }
            },
            yAxis: {
                type: 'value',
            },
            series: [
                {
                    name: 'Total',
                    type: 'bar',
                    barWidth: '45%',
                    data: YOD,
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
            timeRangeText = "Weekly's";
            break;
        case 3:
            timeRangeText = "Monthly's";
            break;
        case 4:
            timeRangeText = "Yearly's";
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
        document.getElementById('maintanceheading_label').textContent = `${timeRangeText} Maintenance`;
        document.getElementById('breakdownheading_label').textContent = `${timeRangeText} Breakdown`;
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
                    itemStyle: { color: 'rgb(140, 217, 201)' },
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
                    itemStyle: { color: 'rgb(140, 217, 201)' },
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
                $('#EnqEQMaintanceDetailsModal').modal('show');

            } 
            catch (error) {
                console.error('Error fetching topSrmsDetailsModal data:', error);
                document.getElementById('topSrmsCompletedDurationDetailsModalBody').innerText = 'Error fetching details.';
            }
                
        });
        breakdownChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
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

                                        
                $('#EnqEQBreakdownDetailsModal').modal('show');

            } catch (error) {
                
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

        document.getElementById('TotalIncident').textContent = roomData.TotalIncident;
        document.getElementById('TotalIncidentPer').textContent = `${roomData.TotalIncidentPer}%`;
        document.getElementById('TotalIncidentProgress').style.width = `${roomData.TotalIncidentPer}%`;
        }
        catch (error) {
            hideLoader(chartType);
            console.error('Error fetching innerhtml data:', error);
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
                    itemStyle: { color: 'rgb(140, 217, 201)' },
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for occupancy bars
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        dpChart.setOption(option);
        

        dpChart.on('click', async function (params) {
            if (params.componentType === 'series') {
            try {
                const srmsRequest=params.name
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

                
                $('#topSrmsCompletedDurationDetailsModal').modal('show');

            } catch (error) {
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
                left: '5%', right: '5%', bottom: '10%', containLabel: true
            },
            xAxis: {
                type: 'category',
                data: CallDescription,
                axisLabel: {
                    interval: 0,
                    rotate: 20,  // Tilts labels for readability
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
                    label: {
                        show: true,
                        position: 'top',
                    }

                },
            ]
        };


        topSRMSChart.setOption(option);
        topSRMSChart.on('click', async function (params) {
        if (params.componentType === 'series') {
        try {
            const srmsRequest=params.name
            const detailResponse = await fetch(`api/RDRoomsSRMSTopRequestDetailsChart/?srmsRequest=${params.name}&RT=${RT}`);
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

            
            $('#topSrmsDetailsModal').modal('show');

        } catch (error) {
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };
        ppmrRoomChart.setOption(option);
        ppmrRoomChart.on('click', async function (params) {
        try {
            const orgId = OrganizationID[params.dataIndex];
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


        $('#PPMCheckListDetailsModal').modal('show');

        } catch (error) {
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };
        trainingChart.setOption(option);
        trainingChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
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
        
                
                $('#TrainingHoursDetailsModal').modal('show');
                
            } catch (error) {
                console.error('Error fetching TrainingHoursDetailsModal data:', error);
                document.getElementById('TrainingHoursDetailsModalBody').innerText = 'Error fetching details.';
            }
                    
            });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}

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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        warningLetChart.setOption(option);
        warningLetChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
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
        
                
                $('#WarningLettersDetailsmodal').modal('show');
                
            } catch (error) {
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        cateringSaleChart.setOption(option);
        cateringSaleChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
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
        
                
                $('#cateringSalesEventDetailsmodal').modal('show');
                
            } catch (error) {
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        breakageChart.setOption(option);
        breakageChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
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
        
                
                $('#DailyBreakageDetails').modal('show');
                
            } catch (error) {
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };


        restaurantFeedbackChart.setOption(option);
        restaurantFeedbackChart.on('click', async function (params) {
            try {
                const orgId = OrganizationID[params.dataIndex];
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
        
                
                $('#DailyBreakageDetails').modal('show');
                
            } catch (error) {
                console.error('Error fetching DailyBreakageDetails data:', error);
                document.getElementById('DailyBreakageDetailsBody').innerText = 'Error fetching details.';
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
        guestChart.on('click', async function (params) {
                try {
                    const orgId = OrganizationID[params.dataIndex];
                    const MetOn = params.seriesName
                    
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
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

                
                $('#totalSRMSDetailsModal').modal('show');
            }
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
                    label: {
                        show: true,
                        position: 'top',
                    }
                },
            ]
        };

       
        outOfOrderChart.setOption(option);
        outOfOrderChart.on('click', async function (params) {
        if (params.componentType === 'series') {
            const orgId = OrganizationID[params.dataIndex]; // Get OrganizationID based on the clicked bar
            await openModal(orgId,Selected_RT); // Open modal with Organization ID
        }
        });
    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }
}

async function openModal(orgId,RT) {
    try {
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

        
        $('#OutOfOrderModal').modal('show');

    } catch (error) {
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
        document.getElementById('modalDSRHotelName').textContent = clickedHotel; // Update hotel name
        document.getElementById('modalDSRTotalVisit').textContent = totalVisit;
        
        if (detailsJson) {
            const detailsArray = JSON.parse(detailsJson); 
         
            const tableBody = document.getElementById('dsrdetailContent');
            tableBody.innerHTML = '';

            detailsArray.forEach(detail => {
                const companyDetailsArray = detail.am;

                companyDetailsArray.forEach(companyDetails => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
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

            
            $('#dsrDetails').modal('show');
        }
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },
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
        paymasterChart.on('click', async function (params) {
        try {
            const orgId = OrganizationID[params.dataIndex];
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

            $('#PayMasterModal').modal('show');
        
        } catch (error) {
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
                data: ['Total', 'Active', 'Expired']  // Add 'Total' to the legend
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
                    itemStyle: { color: 'rgb(95, 75, 139)' },  // Color for total contracts
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
        saleChart.on('click', async function (params) {
        if (params.componentType === 'series') {
        const orgId = OrganizationID[params.dataIndex]; 
            const status = params.seriesName;  
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
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
        ArcollectionChart.on('click', async function (params) {
        try {
            const orgId = OrganizationID[params.dataIndex];
            const detailResponse = await fetch(`api/GMArCollection/?OrganizationID=${orgId}&RT=${RT}`);
            if (!detailResponse.ok) throw new Error('Network response was not ok ' + detailResponse.statusText);

            const detailData = await detailResponse.json();
            const toprequestbody = document.getElementById('ARCollectionModalBody');


            toprequestbody.innerHTML = ''; 

            detailData.Table.forEach(detail => {
            document.getElementById('sp_arC_LastupdateDate').textContent=detail.LastupdateDate
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="width:170px">${detail.Account} 
                </td>
                <td style="text-align:right">${detail.Day91}</td>
                <td style="text-align:right">${detail.TotalPending}</td>

            `;
            toprequestbody.appendChild(row);
            });

            
                    $('#ARCollectionModal').modal('show');
        
        } catch (error) {
            console.error('Error fetching ARCollectionModal data:', error);
            document.getElementById('ARCollectionModalBody').innerText = 'Error fetching details.';
        }    
        });

    } catch (error) {
        hideLoader(chartType);
        console.error('Error fetching paymasterChart  data:', error);
    }
}



document.getElementById('revenueHeading').addEventListener('click', async function () {
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

    const Type = 'Total Revenue'

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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
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
    } catch (error) {
        console.error('Error fetching TopSRMSrequestChart data:', error);
    }


});



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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
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
                    itemStyle: { color: 'rgb(95, 75, 139)' }, // Color for out-of-order bars
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


