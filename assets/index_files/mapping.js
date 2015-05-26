jQuery(document).ready(function() {
	var mappingFile = 'mapping.txt';
	var dvFile = 'dv.txt';
	var lines = [];
	jQuery.get(mappingFile, function(data) {
		lines = data.split(/\r\n|\r|\n/g);

		var pairs = [];
		var DV2Q = [];
		var DV2V = [];
		var lonelyVars = [];
		var lonelyQID = [];
		for (var i = 0; i < lines.length; i++) {
			var pieces = lines[i].split("\t");
			if (pieces[0] == '0' || pieces[1] == '0') {
				if (pieces[0] == '0')
					lonelyVars[lonelyVars.length] = pieces[1]
				/*if (pieces[1] == '0')
					lonelyQID[lonelyQID.length] = pieces[0]*/
				continue;
			}
			pairs[pairs.length] = {
				QID: pieces[0],
				Var: pieces[1]
			};
		}
		
		jQuery.ajax({
			url: dvFile,
			dataType : 'text',
			async: false,
			success: function(dv) {
				dv_lines = dv.split(/\r\n|\r|\n/g);
				for (var i = 0; i < dv_lines.length; i++) {
					var pieces = dv_lines[i].split("\t");
					if (typeof pieces[1] == 'undefined') continue;
					if (pieces[1].substr(0,3) == 'qc_') {
						DV2Q[DV2Q.length] = {
							DV: 	pieces[0],
							QID:	pieces[1]
						};
					} else {
						DV2V[DV2V.length] = {
							DV: 	pieces[0],
							V:		pieces[1],
							QID:	[]
						};
					}
					for (var j = 0; j < lonelyVars.length; j++) {
						if (lonelyVars[j] == pieces[0]) {
							lonelyVars.splice(j, 1);
							j--;
						}
					}
				}
				for (var sweep = 0; sweep < 5; sweep++) {
					for (var i = 0; i < DV2V.length; i++) {
						if (DV2V[i].QID.length < 1) {
							for (var j = 0; j < pairs.length; j++) {
								if (pairs[j].Var == DV2V[i].V) {
									DV2V[i].QID[DV2V[i].QID.length] = pairs[j].QID;
								}
							}
							for (var j = 0; j < DV2Q.length; j++) {
								if (DV2Q[j].DV == DV2V[i].V) {
									DV2V[i].QID[DV2V[i].QID.length] = DV2Q[j].QID;
								}
							}
							for (var j = 0; j < DV2V.length; j++) {
								if (i == j) continue;
								if (DV2V[j].DV == DV2V[i].V) {
									DV2V[i].QID = DV2V[i].QID.concat(DV2V[j].QID);
								}
							}
						}
					}
				}
			}
		});

		jQuery('span.CcQuestion').each(function() {
			var vars= [];
			var dv_q= [];
			var dv_v= [];
			var cells = [];
			var cells_q = [];
			var cells_v = [];
			for (var i = 0; i < pairs.length; i++) {
				var Qc = pairs[i].QID;
				var GridRef = null;
				var pieces = pairs[i].QID.split("$");
				if (pieces.length > 1) {
					Qc = pieces[0];
					GridRef = pieces[1];
				}

				if (Qc == jQuery(this).attr('id')) {
					if (GridRef == null) {
						vars[vars.length] = pairs[i].Var;
					} else {
						var coords = GridRef.split(";");
						if (typeof cells[Number(coords[1])] != "object")
							cells[Number(coords[1])] = [];
						if (typeof cells[Number(coords[1])][Number(coords[0])] != "object")
							cells[Number(coords[1])][Number(coords[0])] = [];
						cells[Number(coords[1])][Number(coords[0])][cells[Number(coords[1])][Number(coords[0])].length] = pairs[i].Var;

					}
				}
			}
			
			for (var i = 0; i < DV2Q.length; i++) {
				var Qc = DV2Q[i].QID;
				var GridRef = null;
				var pieces = DV2Q[i].QID.split("$");
				if (pieces.length > 1) {
					Qc = pieces[0];
					GridRef = pieces[1];
				}

				if (Qc == jQuery(this).attr('id')) {
					if (GridRef == null) {
						dv_q[dv_q.length] = DV2Q[i].DV;
					} else {
						var coords = GridRef.split(";");
						if (typeof cells_q[Number(coords[1])] != "object")
							cells_q[Number(coords[1])] = [];
						if (typeof cells_q[Number(coords[1])][Number(coords[0])] != "object")
							cells_q[Number(coords[1])][Number(coords[0])] = [];
						cells_q[Number(coords[1])][Number(coords[0])][cells_q[Number(coords[1])][Number(coords[0])].length] = DV2Q[i].DV;

					}
				}
			}
			
			for (var i = 0; i < DV2V.length; i++) {
				console.log(DV2V[i]);
				for (var j = 0; j < DV2V[i].QID.length; j++) {
					var Qc = DV2V[i].QID[j];
					var GridRef = null;
					var pieces = DV2V[i].QID[j].split("$");
					if (pieces.length > 1) {
						Qc = pieces[0];
						GridRef = pieces[1];
					}

					if (Qc == jQuery(this).attr('id')) {
						if (GridRef == null) {
							dv_v[dv_v.length] = DV2V[i].DV;
						} else {
							var coords = GridRef.split(";");
							if (typeof cells_v[Number(coords[1])] != "object")
								cells_v[Number(coords[1])] = [];
							if (typeof cells_v[Number(coords[1])][Number(coords[0])] != "object")
								cells_v[Number(coords[1])][Number(coords[0])] = [];
							cells_v[Number(coords[1])][Number(coords[0])][cells_v[Number(coords[1])][Number(coords[0])].length] = DV2V[i].DV;

						}
					}
				}
			}
			
			var linked = false;
			if (vars.length > 0 || dv_q.length > 0 || dv_v.length > 0) {
				jQuery(this).append('&nbsp;<span class="Variables padded">Variables = ' + 
					vars.join(', ') + 
					(vars.length > 0 && dv_q.length + dv_v.length > 0 ? ', ' : '') + 
					'<span class="DV2Q">' +
					dv_q.join(', ') +
					(dv_q.length > 0 && dv_v.length > 0 ? ', ' : '') + 
					'</span><span class="DV2V">' +
					dv_v.join(', ') +
					'</span></span>');
				linked = true;
			}
			if (cells.length > 0 || cells_q > 0 || cells_v > 0) {
				var rowCounter = 0;
				jQuery(this).parent().next().find('table tr').each(function() {
					var answers = jQuery(this).children('td.answer');
					if (answers.length > 0) {
						rowCounter++;
						if (typeof cells[rowCounter] == "object") {
							var colCounter = 0;
							answers.each(function() {
								colCounter++;
								if (typeof cells[rowCounter][colCounter] == "object")
									jQuery(this).html('<span class="Variables">' + cells[rowCounter][colCounter].join(', ') + '</span>');
							});
						}
						if (typeof cells_q[rowCounter] == "object") {
							var colCounter = 0;
							answers.each(function() {
								colCounter++;
								if (typeof cells_q[rowCounter][colCounter] == "object") {
									if (jQuery(this).children('.Variables').first().html().length > 0)
										jQuery(this).children('.Variables').first().append(', ');
									jQuery(this).children('.Variables').first().append('<span class="DV2Q">' + cells_q[rowCounter][colCounter].join(', ') + '</span>');
								}
							});
						}
						if (typeof cells_v[rowCounter] == "object") {
							var colCounter = 0;
							answers.each(function() {
								colCounter++;
								if (typeof cells_v[rowCounter][colCounter] == "object") {
									if (jQuery(this).children('.Variables').first().html().length > 0)
										jQuery(this).children('.Variables').first().append(', ');
									jQuery(this).children('.Variables').first().append('<span class="DV2V">' + cells_v[rowCounter][colCounter].join(', ') + '</span>');
								}
							});
						}
					}	
				});
				linked = true;
			}
			if (!linked) {
				lonelyQID[lonelyQID .length] = jQuery(this).attr('id')
			}
		});
		jQuery('span.Variables').css({
			color : 'blue'
		});
		jQuery('span.Variables span.DV2Q').css({
			color: 'green'
		});
		jQuery('span.Variables span.DV2V').css({
			color: 'red'
		});
		jQuery('span.padded').css({
			marginLeft: '40px'
		});


		
		jQuery('#wrapper').after(function() {
			output = jQuery(document.createElement('div'))
				.attr('id', 'mapping-results')
				.append(jQuery(document.createElement('div'))
					.css({width: '50%', float: 'left'})
					.append('<h4>Unmapped Variables</h4>')
					.append(jQuery(document.createElement('ul'))
						.html('<li>' + lonelyVars.join('</li><li>') + '</li>')
					)
				)
				.append(jQuery(document.createElement('div'))
					.css({width: '50%', float: 'right'})
					.append('<h4>Unmapped Questions</h4>')
					.append(jQuery(document.createElement('ul'))
						.html('<li>' + lonelyQID.join('</li><li>') + '</li>')
					)
				);

			return output;
		});
		jQuery('#mapping-results').css({
			maxWidth : '940px',
			margin: '0px auto',
			backgroundColor: 'white',
			borderWidth: '1px',
			borderStyle: 'solid',
			padding: '20px',
			marginTop: '40px',
			overflow: 'hidden'
		});

	}, 'text');

});