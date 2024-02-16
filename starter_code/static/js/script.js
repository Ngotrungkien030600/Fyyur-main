window.parseISOString = function(s) {
  const [year, month, day, hours, minutes, seconds, milliseconds] = s.split(/\D+/);
  return new Date(Date.UTC(year, month - 1, day, hours, minutes, seconds, milliseconds));
};
