function downloadTicket(id) {
    const ticket = document.getElementById(id);
    if (!ticket) {
        alert("Ticket not found!");
        return;
    }

    const ticketClone = ticket.cloneNode(true);

    // ✅ Hide button ONLY in PDF
    const cloneButton = ticketClone.querySelector(".download-btn");
    if (cloneButton) {
        cloneButton.style.display = "none";
    }

    ticketClone.style.position = "fixed";
    ticketClone.style.top = "0";
    ticketClone.style.left = "0";
    ticketClone.style.opacity = "1";
    ticketClone.style.pointerEvents = "none";
    ticketClone.style.zIndex = "9999";
    ticketClone.style.background = "#fff";

    document.body.appendChild(ticketClone);

    setTimeout(() => {
        html2canvas(ticketClone, { scale: 1.5, useCORS: true, backgroundColor: "#ffffff" })
            .then(canvas => {
                const imgData = canvas.toDataURL("image/png");

                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });

                const pdfWidth = pdf.internal.pageSize.getWidth();
                const width = pdfWidth * 0.7;
                const height = (canvas.height * width) / canvas.width;
                const marginX = (pdfWidth - width) / 2;

                pdf.addImage(imgData, "PNG", marginX, 10, width, height);
                pdf.save(id + ".pdf");

                document.body.removeChild(ticketClone);
            })
            .catch(err => {
                console.error("PDF generation error:", err);
                document.body.removeChild(ticketClone);
            });
    }, 200);
}







// function downloadTicket(id) {
//     const ticket = document.getElementById(id);
//     if (!ticket) {
//         alert("Ticket not found!");
//         return;
//     }

//     // Clone the ticket to avoid reusing the same node
//     const ticketClone = ticket.cloneNode(true);
//     ticketClone.style.position = "fixed";
//     ticketClone.style.top = "0";
//     ticketClone.style.left = "0";
//     ticketClone.style.opacity = "1"; // visible to canvas
//     ticketClone.style.pointerEvents = "none";
//     ticketClone.style.zIndex = "9999";
//     ticketClone.style.background = "#fff";
//     document.body.appendChild(ticketClone);

//     setTimeout(() => {
//         html2canvas(ticketClone, { scale: 1.5, useCORS: true, backgroundColor: "#ffffff" })
//             .then(canvas => {
//                 const imgData = canvas.toDataURL("image/png");

//                 const { jsPDF } = window.jspdf;
//                 const pdf = new jsPDF({ orientation: "portrait", unit: "mm", format: "a4" });

//                 const pdfWidth = pdf.internal.pageSize.getWidth();  // 210mm for A4
//                 const pdfHeight = pdf.internal.pageSize.getHeight(); // 297mm for A4

//                 // Set ticket width to 70% of page width
//                 const width = pdfWidth * 0.7;
//                 const height = (canvas.height * width) / canvas.width; // scale height proportionally

//                 // Center horizontally
//                 const marginX = (pdfWidth - width) / 2;
//                 const marginY = 10; // top margin (adjust if needed)

//                 pdf.addImage(imgData, "PNG", marginX, marginY, width, height);
//                 pdf.save(id + ".pdf");

//                 document.body.removeChild(ticketClone);
//             })
//             .catch(err => {
//                 console.error("PDF generation error:", err);
//                 document.body.removeChild(ticketClone);
//             });
//     }, 200);
// }




// // async function downloadTicket(id) {

// //     const ticket = document.getElementById(id);

// //     if (!ticket) {
// //         alert("Ticket not found!");
// //         return;
// //     }

// //     // Small delay to allow proper rendering
// //     await new Promise(resolve => setTimeout(resolve, 300));

// //     const opt = {
// //         margin: 0.5,
// //         filename: id + '.pdf',   // Unique filename
// //         image: { type: 'jpeg', quality: 0.98 },
// //         html2canvas: { 
// //             scale: 2,
// //             useCORS: true
// //         },
// //         jsPDF: { 
// //             unit: 'in', 
// //             format: 'a4', 
// //             orientation: 'portrait' 
// //         }
// //     };

// //     await html2pdf().set(opt).from(ticket).save();
// // }