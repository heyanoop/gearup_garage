document.addEventListener('DOMContentLoaded', function() {
    const downloadPdfBtn = document.getElementById('download-button');

    function generatePDF() {
        const doc = new jsPDF();

        doc.text('Sales Report', 10, 10);

        const table = document.getElementById('sales-table');
        const data = Array.from(table.rows).map(row => Array.from(row.cells).map(cell => cell.innerText));

        const startY = 20;
        doc.autoTable({
            head: [data[0]],
            body: data.slice(1),
            startY: startY
        });

        doc.save('sales_report.pdf');
    }

    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener('click', generatePDF);
    }
});
