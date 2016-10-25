# KiCad_BOM_Editor
Export component fields as CVS and import CVS to add/change/remove field values and names. Based on BPJWES/KiCAD_Partslist_editor, whithout restriction to fieldnames. Working concept, not a finished product.

Fieldnames are automaticly found, and orderd. So this should work with any field naming method.

Working import:
If macht between CVS and kicad schematic is found the field names (CVS collum name) and values are set as is in CVS. Empty cels are omitted. Can be used to change a field name in all components. Allows the change of reference (if matched by timestamp).

# TODO:
- Clean up code
- Add choiche for import by reference and/or timestamp (now forced to timestamp)
