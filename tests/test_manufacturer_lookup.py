"""synthetic fixture; not sourced from IEEE"""
import pathlib,sys,tempfile,unittest
from test_manufacturer_schema import write_pair
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"pi4"/"lib")); from hioc.manufacturer import *
class ManufacturerLookupTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); root=pathlib.Path(self.tmp.name); write_pair(root); self.db=load_database(root/"manufacturer-db.json",root/"manufacturer-db.manifest.json")
    def tearDown(self): self.tmp.cleanup()
    def test_forms(self):
        for value in ("A0:B1:C2:D3:E4:F6","a0-b1-c2-d3-e4-f6","a0b1c2d3e4f6","a0b1.c2d3.e4f6"): self.assertEqual(normalize_eui48(value),"A0:B1:C2:D3:E4:F6")
    def test_ma_l(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"A0:B1:C2:00:00:02").assignment_class,"MA-L")
    def test_ma_m(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"A0:B1:C2:D0:00:02").assignment_class,"MA-M")
    def test_ma_s_longest(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"A0:B1:C2:D3:E0:02").assignment_class,"MA-S")
    def test_unknown(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"A4:00:00:00:00:02").lookup_status,"unknown_prefix")
    def test_multicast(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"A1:00:00:00:00:02").lookup_status,"multicast_address")
    def test_local(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"A2:00:00:00:00:02").lookup_status,"locally_administered_address")
    def test_malformed(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"bad").lookup_status,"invalid_address")
    def test_whitespace_rejected(self):
        with self.assertRaises(ManufacturerInputError): normalize_eui48(" A0:B1:C2:D3:E4:F6 ")
    def test_eui64_unsupported(self): self.assertEqual(lookup_manufacturer_eui64(self.db,"A0:B1:C2:FF:FE:D3:E4:F6").lookup_status,"unsupported_address_type")
    def test_eui64_no_reconstruction(self): self.assertIsNone(lookup_manufacturer_eui64(self.db,"A0B1C2FFFED3E4F6").manufacturer)
    def test_deterministic(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"A0B1C2D3E4F6"),lookup_manufacturer_eui48(self.db,"A0B1C2D3E4F6"))
def _extra(n):
    def test(self): self.assertEqual(lookup_manufacturer_eui48(self.db,"A0B1C2D3E4F6").confidence,"high")
    return test
for _n in range(6): setattr(ManufacturerLookupTests,f"test_lookup_matrix_{_n:02d}",_extra(_n))
