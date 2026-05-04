export function polar(cx, cy, r, angle) {
  // console.log(cx, cy, r, angle);
  let rad = ((angle - 90) * Math.PI) / 180;
  return {
    x: cx + r * Math.cos(rad),
    y: cy + r * Math.sin(rad),
  };
}

export function donutSlicePath(cx, cy, r1, r2, start, end) {
  let p1 = polar(cx, cy, r2, start);
  let p2 = polar(cx, cy, r2, end);
  let p3 = polar(cx, cy, r1, end);
  let p4 = polar(cx, cy, r1, start);

  let large = Math.abs(end - start) > 180 ? 1 : 0;

  return `
        M ${p1.x} ${p1.y}
        A ${r2} ${r2} 0 ${large} 1 ${p2.x} ${p2.y}
        L ${p3.x} ${p3.y}
        A ${r1} ${r1} 0 ${large} 0 ${p4.x} ${p4.y}
        Z
    `;
}

export function arcPath(cx, cy, r, start, end) {
  let p1 = polar(cx, cy, r, start);
  let p2 = polar(cx, cy, r, end);
  let midAngle = (start + end) / 2;

  // Keep reading from left to right
  let sweep = 1;
  if (midAngle > 90 && midAngle < 270) {
    let tmp = p1;
    p1 = p2;
    p2 = tmp;
    sweep = 0;
  }
  let large = Math.abs(end - start) > 180 ? 1 : 0;

  return `
        M ${p1.x} ${p1.y}
        A ${r} ${r} 0 ${large} ${sweep} ${p2.x} ${p2.y}
    `;
}

export function angleFromPoint(cx, cy, x, y) {
  return ((Math.atan2(y - cy, x - cx) * 180) / Math.PI + 90 + 360) % 360;
}
