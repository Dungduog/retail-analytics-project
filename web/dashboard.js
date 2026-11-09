"use strict";

const data = window.RETAIL_DATA;
const byId = (id) => document.getElementById(id);
const integer = new Intl.NumberFormat("vi-VN");
const decimal = new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 1 });
const money = (value) => `£${integer.format(Math.round(value))}`;
const percent = (part, total) => `${decimal.format(100 * part / total)}%`;
const monthLabel = (month) => `${month.slice(5)}/${month.slice(0, 4)}`;
const partialMonth = "2011-12";

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function renderMetrics() {
  const { SalesInvoices, CancelledInvoices, MissingCustomerRows, Rows } = data.summary;
  const gross = data.monthly.reduce((total, row) => total + row.Revenue, 0);
  const customers = data.segments.reduce((total, row) => total + row.Customers, 0);
  const uk = data.countryRevenue.find((row) => row.Country === "United Kingdom").Revenue;
  const metrics = [
    ["Doanh thu gross", `£${decimal.format(gross / 1e6)} triệu`, money(gross)],
    ["Khách định danh", integer.format(customers), "Có mặt trong bảng RFM"],
    ["Hóa đơn bán", integer.format(SalesInvoices), "InvoiceNo bán duy nhất"],
    ["Tỷ lệ hóa đơn hủy", percent(CancelledInvoices, SalesInvoices + CancelledInvoices),
      `${integer.format(CancelledInvoices)} đơn hủy / tổng hóa đơn`],
    ["Doanh thu từ UK", percent(uk, gross), "Tỷ trọng trên gross"],
  ];
  for (const [label, value, note] of metrics) {
    const card = element("article", undefined, "metric");
    card.append(element("h2", label), element("strong", value), element("small", note));
    byId("metrics").append(card);
  }
  byId("missing-customers").textContent =
    `${integer.format(MissingCustomerRows)} dòng (${percent(MissingCustomerRows, Rows)}) thiếu CustomerID.`;
}

function renderChart() {
  const chart = byId("monthly-chart");
  const plot = { left: 62, right: 885, top: 24, bottom: 246 };
  const peak = data.monthly.reduce((best, row) => row.Revenue > best.Revenue ? row : best);
  const step = 250000;
  const ceiling = Math.ceil(peak.Revenue / step) * step;
  const y = (value) => plot.bottom - value / ceiling * (plot.bottom - plot.top);
  const points = data.monthly.map((row, index) => ({
    ...row,
    x: plot.left + index / (data.monthly.length - 1) * (plot.right - plot.left),
    y: y(row.Revenue),
  }));

  function add(tag, attributes, label, parent = chart) {
    const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, value);
    if (label !== undefined) node.textContent = label;
    parent.append(node);
    return node;
  }

  const defs = add("defs", {});
  const gradient = add("linearGradient", { id: "revenue-fill", x2: "0%", y2: "100%" }, undefined, defs);
  add("stop", { offset: "0%", "stop-color": "#357ff0", "stop-opacity": ".35" }, undefined, gradient);
  add("stop", { offset: "100%", "stop-color": "#357ff0", "stop-opacity": ".02" }, undefined, gradient);
  for (let value = 0; value <= ceiling; value += step) {
    add("line", { x1: plot.left, x2: plot.right, y1: y(value), y2: y(value), stroke: "#262b35" });
    add("text", { x: plot.left - 9, y: y(value) + 4, "text-anchor": "end" }, `£${value / 1000}k`);
  }

  const complete = points.filter((row) => row.OrderMonth !== partialMonth);
  const end = complete.at(-1);
  const line = complete.map((row) => `${row.x},${row.y}`).join(" ");
  add("polygon", { points: `${plot.left},${plot.bottom} ${line} ${end.x},${plot.bottom}`, fill: "url(#revenue-fill)" });
  add("polyline", { points: line, fill: "none", stroke: "#62a1ff", "stroke-width": 3, "stroke-linejoin": "round" });
  const partial = points.find((row) => row.OrderMonth === partialMonth);
  if (partial) {
    add("line", { x1: end.x, x2: partial.x, y1: end.y, y2: partial.y,
      stroke: "#efbb64", "stroke-width": 2, "stroke-dasharray": "6 5" });
  }
  for (const row of points) {
    const label = monthLabel(row.OrderMonth) + (row === partial ? "*" : "");
    add("text", { x: row.x, y: 271, "text-anchor": "middle" }, label);
    const dot = add("circle", { cx: row.x, cy: row.y, r: row.Revenue === peak.Revenue ? 6 : 4,
      fill: row === partial ? "#efbb64" : "#86b7ff", stroke: "#131519", "stroke-width": 2 });
    add("title", {}, `${label} · ${money(row.Revenue)}`, dot);
    byId("monthly-values").append(element("li", `${label} · ${money(row.Revenue)}`));
  }
  byId("peak").textContent = `Cao nhất · ${monthLabel(peak.OrderMonth)} · ${money(peak.Revenue)}`;
}

function renderRanking(id, rows, name, metric, format) {
  const maximum = Math.max(1, ...rows.map((row) => row[metric]));
  const items = rows.map((row, index) => {
    const item = element("li");
    const label = element("div", undefined, "rank-line");
    label.append(element("span", String(index + 1).padStart(2, "0")),
      element("span", row[name]), element("strong", format(row[metric])));
    const bar = element("div", undefined, "bar");
    bar.setAttribute("aria-hidden", "true");
    const fill = element("span");
    fill.style.width = `${100 * row[metric] / maximum}%`;
    bar.append(fill);
    item.append(label, bar);
    return item;
  });
  byId(id).replaceChildren(...items);
}

function renderMarkets(metric) {
  const revenue = metric === "Revenue";
  const products = revenue ? data.productRevenue : data.productQuantity;
  const countries = revenue ? data.countryRevenue.slice(0, 10) : data.countryQuantity;
  const format = revenue ? money : (value) => integer.format(value);
  renderRanking("products", products, "Description", metric, format);
  renderRanking("countries", countries, "Country", metric, format);
  byId("ranking-note").textContent = revenue
    ? "Doanh thu gross (GBP). Bảng mã hàng gồm cả mã phí và dịch vụ."
    : "Số đơn vị trên dòng bán. Bảng mã hàng gồm cả mã phí và dịch vụ.";
  for (const button of document.querySelectorAll("[data-metric]")) {
    button.setAttribute("aria-pressed", String(button.dataset.metric === metric));
  }
}

function renderReturns() {
  for (const row of data.cancellations) {
    const card = element("article", undefined, "case");
    card.append(element("strong", `${integer.format(row.Quantity)} chiếc`),
      element("h3", row.Description),
      element("p", `${row.InvoiceNo} → ${row.Cancellation} · ${money(row.Revenue)}`));
    byId("cases").append(card);
  }
  renderRanking("refund-frequency", data.refundFrequency, "Description", "CancelledInvoiceCount", integer.format);
  renderRanking("refund-value", data.refundValue, "Description", "CancelledValue", money);
}

if (data) {
  renderMetrics();
  renderChart();
  renderMarkets("Revenue");
  renderRanking("segments", data.segments, "Segment", "Customers", integer.format);
  renderReturns();
  for (const button of document.querySelectorAll("[data-metric]")) {
    button.addEventListener("click", () => renderMarkets(button.dataset.metric));
  }
  const nav = [...document.querySelectorAll("nav a")];
  const updateNavigation = () => {
    for (const link of nav) {
      link.removeAttribute("aria-current");
      if (link.hash === (location.hash || "#overview")) link.setAttribute("aria-current", "location");
    }
  };
  window.addEventListener("hashchange", updateNavigation);
  updateNavigation();
} else {
  byId("data-error").hidden = false;
}
